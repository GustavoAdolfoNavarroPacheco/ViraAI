import asyncio
from unittest.mock import patch

# Monkeypatch the database URI to use SQLite in-memory before importing database modules
from app.core.config import settings
type(settings).SQLALCHEMY_DATABASE_URI = property(lambda self: "sqlite+aiosqlite:///:memory:")

# Now import the database core and models
from app.core.database import engine, Base, SessionLocal
from app.domain.models import Channel, Post
from app.application.tasks import publish_post_task

async def setup_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def test_publish_post_task_success():
    print("Running test_publish_post_task_success...")
    async with SessionLocal() as db:
        # Create a channel
        channel = Channel(
            platform="twitter",
            name="VIRA Twitter Official",
            is_active=True
        )
        db.add(channel)
        await db.commit()
        await db.refresh(channel)

        # Create a draft post
        post = Post(
            channel_id=channel.id,
            content="Testing VIRA auto-publishing background runner!",
            status="draft"
        )
        db.add(post)
        await db.commit()
        await db.refresh(post)
        
        post_id = post.id

    # Execute the Celery task (runs synchronously since celery is in eager mode locally)
    # Using .apply() ensures it runs in eager mode context and returns EagerResult
    result = publish_post_task.apply(args=[post_id])
    
    assert result.status == "SUCCESS"
    task_value = result.result
    assert task_value["status"] == "success"
    assert task_value["platform"] == "twitter"

    # Verify updates in the database
    async with SessionLocal() as db:
        updated_post = await db.get(Post, post_id)
        assert updated_post is not None
        assert updated_post.status == "published"
        assert updated_post.published_at is not None
        assert updated_post.impressions > 0
        assert updated_post.engagement_rate > 0.0
        print("-> test_publish_post_task_success: PASSED")

async def test_publish_post_task_permanent_failure():
    print("Running test_publish_post_task_permanent_failure...")
    async with SessionLocal() as db:
        # Get existing channel or create one
        channel = Channel(
            platform="linkedin",
            name="VIRA LinkedIn Official",
            is_active=True
        )
        db.add(channel)
        await db.commit()
        await db.refresh(channel)

        # Create a draft post with a trigger that causes permanent failure
        post = Post(
            channel_id=channel.id,
            content="Post triggering fail trigger_fail",
            status="draft"
        )
        db.add(post)
        await db.commit()
        await db.refresh(post)
        
        post_id = post.id

    # Execute the task
    result = publish_post_task.apply(args=[post_id])
    
    # In eager mode, celery task return value of unhandled ValueError will propagate or return failure status
    # In our implementation of tasks.py, we wrap the execution in a try-except block that returns a failure dictionary
    # if it's not a Retry exception.
    task_value = result.result
    assert task_value["status"] == "failed"
    assert "Invalid credentials" in task_value["error"]

    # Verify database state
    async with SessionLocal() as db:
        updated_post = await db.get(Post, post_id)
        assert updated_post is not None
        assert updated_post.status == "failed"
        print("-> test_publish_post_task_permanent_failure: PASSED")

async def test_publish_post_task_retry_mechanism():
    print("Running test_publish_post_task_retry_mechanism...")
    async with SessionLocal() as db:
        channel = Channel(
            platform="twitter",
            name="VIRA X Profile",
            is_active=True
        )
        db.add(channel)
        await db.commit()
        await db.refresh(channel)

        # Create a draft post with trigger_retry
        post = Post(
            channel_id=channel.id,
            content="Temporary rate limit trigger_retry post text",
            status="draft"
        )
        db.add(post)
        await db.commit()
        await db.refresh(post)
        
        post_id = post.id

    # To test the retry mechanism without executing a real retry loop or sleep:
    # We can mock task.retry to assert that it was called.
    with patch("app.application.tasks.publish_post_task.retry") as mock_retry:
        # In eager mode, task.retry raises a Retry exception, let's mock it to raise an exception
        # or do nothing.
        from celery.exceptions import Retry
        mock_retry.side_effect = Retry("Simulated Retry Exception")

        try:
            result = publish_post_task.apply(args=[post_id])
        except Retry:
            pass
        
        # Verify retry was attempted
        assert mock_retry.called
        # Check call arguments
        args, kwargs = mock_retry.call_args
        assert kwargs["countdown"] == 2 # 2^(retry_count + 1) where retry_count=0
        assert "Rate limit exceeded" in str(kwargs["exc"])
        
    print("-> test_publish_post_task_retry_mechanism: PASSED")

async def run_all_tests():
    await setup_test_db()
    await test_publish_post_task_success()
    await test_publish_post_task_permanent_failure()
    await test_publish_post_task_retry_mechanism()

if __name__ == "__main__":
    asyncio.run(run_all_tests())
    print("All Celery task verification tests PASSED successfully!")
