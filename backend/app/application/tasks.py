import asyncio
import datetime
import random
from celery.exceptions import Retry
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.domain.models import Post, Channel
from sqlalchemy.future import select
from app.infrastructure.social_services import SocialService

import threading

# Helper to run async coroutines in Celery synchronous tasks
def run_async(coro):
    try:
        # Check if there is an active running loop
        asyncio.get_running_loop()
        # If yes, run the coroutine in a separate thread to avoid "This event loop is already running"
        result = []
        def target():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result.append(loop.run_until_complete(coro))
            except Exception as ex:
                result.append(ex)
            finally:
                loop.close()
        t = threading.Thread(target=target)
        t.start()
        t.join()
        if isinstance(result[0], Exception):
            raise result[0]
        return result[0]
    except RuntimeError:
        # No running loop, we can run it directly using a new loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()

@celery_app.task(bind=True, max_retries=3)
def publish_post_task(self, post_id: int):
    """
    Celery task to publish a post to its configured channel.
    Includes rate-limiting simulation and exponential backoff retry.
    """
    try:
        return run_async(async_publish_post(self, post_id))
    except Retry:
        # Re-raise Celery's internal Retry exception so Celery handles the retry logic
        raise
    except Exception as e:
        print(f"[Celery Task] Unhandled exception in task: {e}")
        return {"status": "failed", "post_id": post_id, "error": str(e)}

async def async_publish_post(task, post_id: int):
    async with SessionLocal() as db:
        # Fetch post
        result = await db.execute(
            select(Post).where(Post.id == post_id)
        )
        post = result.scalars().first()
        
        if not post:
            print(f"[Celery Task] Post with id {post_id} not found.")
            return {"status": "error", "message": f"Post {post_id} not found"}
            
        # Get channel
        channel_result = await db.execute(
            select(Channel).where(Channel.id == post.channel_id)
        )
        channel = channel_result.scalars().first()
        
        if not channel:
            post.status = "failed"
            await db.commit()
            print(f"[Celery Task] Channel for post {post_id} not found.")
            return {"status": "error", "message": f"Channel for post {post_id} not found"}
            
        print(f"[Celery Task] Attempting to publish post {post_id} to {channel.platform}...")
        
        try:
            # Simulate temporary failure (e.g. rate limit 429) if "trigger_retry" is in post content
            if "trigger_retry" in post.content:
                # Remove trigger string so it doesn't fail on retry
                post.content = post.content.replace("trigger_retry", "").strip()
                await db.commit()
                raise Exception("Rate limit exceeded (simulated temporary 429)")
                
            # Simulate permanent failure (e.g. invalid credentials 401/400) if "trigger_fail" in post content
            if "trigger_fail" in post.content:
                raise ValueError("Invalid credentials or permanent error (400)")

            # Proactive token refresh check
            now = datetime.datetime.now(datetime.timezone.utc)
            if channel.token_expires_at:
                channel_expires_at = channel.token_expires_at
                if channel_expires_at.tzinfo is None:
                    # Convert naive datetime to timezone-aware UTC
                    channel_expires_at = channel_expires_at.replace(tzinfo=datetime.timezone.utc)
                
                if channel_expires_at < now and channel.refresh_token:
                    print(f"[Celery Task] Proactively refreshing token for channel {channel.name}...")
                    try:
                        refresh_data = SocialService.refresh_access_token(channel.platform, channel.refresh_token)
                        channel.auth_token = refresh_data["access_token"]
                        if refresh_data.get("refresh_token"):
                            channel.refresh_token = refresh_data["refresh_token"]
                        expires_in = refresh_data.get("expires_in", 3600)
                        channel.token_expires_at = now + datetime.timedelta(seconds=expires_in)
                        await db.commit()
                        print(f"[Celery Task] Proactive refresh success.")
                    except Exception as re:
                        print(f"[Celery Task] Proactive refresh failed: {re}. Trying default token.")

            # Attempt publish via SocialService
            try:
                publish_result = SocialService.publish_post(
                    platform=channel.platform,
                    access_token=channel.auth_token,
                    content=post.content,
                    media_url=post.media_url
                )
            except ValueError as ve:
                err_msg = str(ve)
                # If error is 401 Unauthorized, reactively refresh token and retry
                if "HTTP Error 401" in err_msg and channel.refresh_token:
                    print(f"[Celery Task] Reactively refreshing token for channel {channel.name}...")
                    try:
                        refresh_data = SocialService.refresh_access_token(channel.platform, channel.refresh_token)
                        channel.auth_token = refresh_data["access_token"]
                        if refresh_data.get("refresh_token"):
                            channel.refresh_token = refresh_data["refresh_token"]
                        expires_in = refresh_data.get("expires_in", 3600)
                        channel.token_expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expires_in)
                        await db.commit()
                        
                        # Retry publish
                        print(f"[Celery Task] Token refreshed. Retrying publish...")
                        publish_result = SocialService.publish_post(
                            platform=channel.platform,
                            access_token=channel.auth_token,
                            content=post.content,
                            media_url=post.media_url
                        )
                    except Exception as refresh_err:
                        print(f"[Celery Task] Reactive refresh or retry failed: {refresh_err}")
                        raise ValueError(f"Publish failed: {err_msg} and token refresh/retry failed: {refresh_err}")
                else:
                    raise

            # Update post status to published
            post.status = "published"
            post.published_at = datetime.datetime.now(datetime.timezone.utc)
            
            # Generate mock engagement metrics
            post.impressions = random.randint(100, 5000)
            post.engagement_rate = round(random.uniform(0.5, 8.5), 2)
            
            await db.commit()
            print(f"[Celery Task] Post {post_id} published successfully on {channel.platform}!")
            return {
                "status": "success", 
                "post_id": post_id, 
                "platform": channel.platform,
                "external_post_id": publish_result.get("post_id"),
                "external_url": publish_result.get("url")
            }
            
        except Exception as e:
            # Check if this is a temporary failure and we can retry
            is_temporary = not isinstance(e, ValueError)
            
            if is_temporary and task.request.retries < task.max_retries:
                # Calculate backoff: e.g. 2, 4, 8 seconds
                countdown = 2 ** (task.request.retries + 1)
                print(f"[Celery Task] Temporary error publishing post {post_id}: {e}. Retrying in {countdown}s (retry {task.request.retries + 1}/{task.max_retries})...")
                
                # Make sure we commit any DB modifications (like stripping trigger_retry)
                await db.commit()
                
                # Raise celery retry
                task.retry(exc=e, countdown=countdown)
            else:
                print(f"[Celery Task] Permanent error or max retries reached publishing post {post_id}: {e}")
                post.status = "failed"
                await db.commit()
                return {"status": "failed", "post_id": post_id, "error": str(e)}
