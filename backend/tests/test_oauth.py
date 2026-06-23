import asyncio
import os
from unittest.mock import patch

# Monkeypatch the database URI to use a file-based SQLite DB before importing database and main modules
from app.core.config import settings
DB_PATH = "./test_oauth.db"
type(settings).SQLALCHEMY_DATABASE_URI = property(lambda self: f"sqlite+aiosqlite:///{DB_PATH}")

from app.core.database import engine, Base, SessionLocal
from app.domain.models import Channel
from fastapi.testclient import TestClient
from app.main import app

async def setup_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

def test_oauth_routes():
    # Setup database
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_test_db())

    client = TestClient(app)

    # 1. Test connect route redirects
    print("Testing connect route redirect...")
    response = client.get("/api/v1/channels/connect/linkedin", follow_redirects=False)
    assert response.status_code == 307 or response.status_code == 302
    target_url = response.headers.get("location")
    assert "code=mock_linkedin_code" in target_url
    print("-> Connect route redirect: PASSED")

    # 2. Test callback route exchanges code, saves to database, and redirects to frontend
    print("Testing callback route...")
    response_cb = client.get(
        "/api/v1/channels/callback/linkedin?code=mock_linkedin_code_test&state=state_123",
        follow_redirects=False
    )
    assert response_cb.status_code == 307 or response_cb.status_code == 302
    frontend_redirect = response_cb.headers.get("location")
    assert "http://localhost:3000/dashboard" in frontend_redirect
    assert "connected=true" in frontend_redirect
    assert "platform=linkedin" in frontend_redirect
    print("-> Callback route redirect: PASSED")

    # Verify that the channel was saved in the database
    async def verify_saved_channel():
        async with SessionLocal() as db:
            from sqlalchemy import select
            result = await db.execute(
                select(Channel).where(Channel.platform == "linkedin")
            )
            channel = result.scalars().first()
            assert channel is not None
            assert channel.name == "Mock Linkedin Creator"
            assert "mock_access_token_linkedin" in channel.auth_token
            assert "mock_refresh_token_linkedin" in channel.refresh_token
            assert channel.token_expires_at is not None
            assert channel.profile_url == "https://linkedin.com/mock_profile"
            assert channel.is_active is True

    loop.run_until_complete(verify_saved_channel())
    print("-> Channel database persistence: PASSED")

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
    test_oauth_routes()
    print("All OAuth routes verification tests PASSED successfully!")
