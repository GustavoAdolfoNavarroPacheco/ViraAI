import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.domain.models import Post, Channel
from app.domain.schemas import PostCreate, PostUpdate, PostResponse, ChannelResponse
from app.application.tasks import publish_post_task

router = APIRouter(
    tags=["campaigns-posts"]
)

# --- Channels List ---
@router.get("/channels", response_model=List[ChannelResponse])
async def list_channels(db: AsyncSession = Depends(get_db)):
    """
    Returns a list of all connected social media channels in VIRA.
    """
    result = await db.execute(select(Channel))
    return result.scalars().all()

# --- Posts CRUD ---
@router.get("/posts", response_model=List[PostResponse])
async def list_posts(status: Optional[str] = None, channel_id: Optional[int] = None, db: AsyncSession = Depends(get_db)):
    """
    Lists posts from the database with optional filter parameters.
    """
    query = select(Post)
    if status:
        query = query.where(Post.status == status)
    if channel_id:
        query = query.where(Post.channel_id == channel_id)
    query = query.order_by(Post.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/posts", response_model=PostResponse)
async def create_post(payload: PostCreate, db: AsyncSession = Depends(get_db)):
    """
    Creates a new post draft associated with a channel.
    """
    # Verify channel exists
    channel_result = await db.execute(select(Channel).where(Channel.id == payload.channel_id))
    channel = channel_result.scalars().first()
    if not channel:
        raise HTTPException(status_code=400, detail=f"Channel {payload.channel_id} not found")
        
    post = Post(
        channel_id=payload.channel_id,
        content=payload.content,
        media_url=payload.media_url,
        scheduled_for=payload.scheduled_for,
        status="draft"
    )
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

@router.patch("/posts/{post_id}", response_model=PostResponse)
async def update_post(post_id: int, payload: PostUpdate, db: AsyncSession = Depends(get_db)):
    """
    Updates post content, media, scheduled date, or state (e.g. Kanban columns).
    """
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found")
        
    trigger_publishing = False
    
    if payload.content is not None:
        post.content = payload.content
    if payload.media_url is not None:
        post.media_url = payload.media_url
    if payload.scheduled_for is not None:
        post.scheduled_for = payload.scheduled_for
    if payload.status is not None:
        # If moving to published, trigger Celery task
        if payload.status == "published" and post.status != "published":
            trigger_publishing = True
        post.status = payload.status
        
    await db.commit()
    await db.refresh(post)
    
    if trigger_publishing:
        publish_post_task.delay(post.id)
        
    return post

@router.post("/posts/{post_id}/publish")
async def trigger_publish(post_id: int, db: AsyncSession = Depends(get_db)):
    """
    Enqueues post publishing on Celery worker.
    Supports countdown execution if scheduled_for is set in the future.
    """
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found")
        
    # Schedule or run immediately
    if post.scheduled_for:
        now = datetime.datetime.now(datetime.timezone.utc)
        scheduled_utc = post.scheduled_for
        if scheduled_utc.tzinfo is None:
            scheduled_utc = scheduled_utc.replace(tzinfo=datetime.timezone.utc)
            
        delay_seconds = int((scheduled_utc - now).total_seconds())
        if delay_seconds > 0:
            publish_post_task.apply_async(args=[post.id], countdown=delay_seconds)
            post.status = "scheduled"
            await db.commit()
            print(f"[API Post Publish] Post {post_id} scheduled in {delay_seconds} seconds.")
            return {"status": "scheduled", "message": f"Post scheduled for publication in {delay_seconds} seconds"}
            
    # Immediate execution
    publish_post_task.delay(post.id)
    post.status = "scheduled"
    await db.commit()
    print(f"[API Post Publish] Post {post_id} immediate queue triggered.")
    return {"status": "queued", "message": "Post publishing task queued in Celery successfully"}

@router.delete("/posts/{post_id}")
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    """
    Deletes the post from the database.
    """
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found")
    await db.delete(post)
    await db.commit()
    print(f"[API Post Delete] Deleted post {post_id}.")
    return {"status": "deleted", "message": f"Post {post_id} deleted successfully"}
