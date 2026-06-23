import asyncio
import os
from unittest.mock import patch

# Monkeypatch the database URI to use a file-based SQLite DB before importing database and main modules
from app.core.config import settings
DB_PATH = "./test_posts.db"
type(settings).SQLALCHEMY_DATABASE_URI = property(lambda self: f"sqlite+aiosqlite:///{DB_PATH}")

from app.core.database import engine, Base, SessionLocal
from app.domain.models import Channel, Post
from fastapi.testclient import TestClient
from app.main import app

async def setup_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

def test_post_routes_flow():
    # Setup test DB
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_test_db())

    client = TestClient(app)

    # 1. Populate a mock channel in the database
    async def create_mock_channel():
        async with SessionLocal() as db:
            channel = Channel(
                platform="twitter",
                name="VIRA Twitter Test Profile",
                profile_url="https://twitter.com/vira_test",
                is_active=True
            )
            db.add(channel)
            await db.commit()
            await db.refresh(channel)
            return channel.id

    channel_id = loop.run_until_complete(create_mock_channel())
    print(f"Created mock channel with ID: {channel_id}")

    # 2. Test GET /channels
    print("Testing GET /channels...")
    response = client.get("/api/v1/channels")
    assert response.status_code == 200
    channels_list = response.json()
    assert len(channels_list) == 1
    assert channels_list[0]["name"] == "VIRA Twitter Test Profile"
    print("-> GET /channels: PASSED")

    # 3. Test POST /posts (Create Draft)
    print("Testing POST /posts (create draft)...")
    payload = {
        "channel_id": channel_id,
        "content": "My first automated post draft with Celery backend!",
        "media_url": "http://example.com/banner.jpg"
    }
    response = client.post("/api/v1/posts", json=payload)
    assert response.status_code == 200
    post_data = response.json()
    assert post_data["id"] is not None
    assert post_data["content"] == payload["content"]
    assert post_data["status"] == "draft"
    post_id = post_data["id"]
    print(f"-> POST /posts: PASSED (Post ID: {post_id})")

    # 4. Test GET /posts
    print("Testing GET /posts...")
    response = client.get("/api/v1/posts")
    assert response.status_code == 200
    posts_list = response.json()
    assert len(posts_list) == 1
    assert posts_list[0]["id"] == post_id
    print("-> GET /posts: PASSED")

    # 5. Test PATCH /posts/{id} (Update draft)
    print("Testing PATCH /posts/{id} (update content)...")
    patch_payload = {
        "content": "My updated post content!",
        "media_url": "http://example.com/new_banner.jpg"
    }
    response = client.patch(f"/api/v1/posts/{post_id}", json=patch_payload)
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["content"] == patch_payload["content"]
    assert updated_data["media_url"] == patch_payload["media_url"]
    print("-> PATCH /posts: PASSED")

    # 6. Test POST /posts/{id}/publish (Queue in Celery)
    print("Testing POST /posts/{id}/publish (queue)...")
    with patch("app.infrastructure.routers.post_routes.publish_post_task.delay") as mock_delay:
        response = client.post(f"/api/v1/posts/{post_id}/publish")
        assert response.status_code == 200
        pub_response = response.json()
        assert pub_response["status"] == "queued"
        assert mock_delay.called
        # Check call arguments
        mock_delay.assert_called_once_with(post_id)
        
    print("-> POST /posts/{id}/publish: PASSED")

    # 7. Test DELETE /posts/{id}
    print("Testing DELETE /posts/{id}...")
    response = client.delete(f"/api/v1/posts/{post_id}")
    assert response.status_code == 200
    del_response = response.json()
    assert del_response["status"] == "deleted"

    # Verify post is removed from database
    async def verify_post_deleted():
        async with SessionLocal() as db:
            p = await db.get(Post, post_id)
            assert p is None

    loop.run_until_complete(verify_post_deleted())
    print("-> DELETE /posts: PASSED")

    # Cleanup database file
    async def shutdown_db():
        await engine.dispose()
    loop.run_until_complete(shutdown_db())
    
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception as e:
            print(f"Warning: Could not remove test database file {DB_PATH}: {e}")

if __name__ == "__main__":
    test_post_routes_flow()
    print("All Campaigns & Channels REST route tests PASSED successfully!")
