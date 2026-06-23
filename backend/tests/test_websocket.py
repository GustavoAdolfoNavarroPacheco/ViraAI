import asyncio
import os
import time
from unittest.mock import patch

# Monkeypatch the database URI to use a file-based SQLite DB before importing database and main modules
from app.core.config import settings
DB_PATH = "./test_ws.db"
type(settings).SQLALCHEMY_DATABASE_URI = property(lambda self: f"sqlite+aiosqlite:///{DB_PATH}")

from app.core.database import engine, Base, SessionLocal
from app.domain.models import Interaction
from fastapi.testclient import TestClient
from app.main import app

async def setup_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

def test_websocket_flow():
    # Run the async setup of test DB
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_test_db())

    client = TestClient(app)
    chat_id = "test_user_999"

    print("Connecting to WebSocket...")
    with client.websocket_connect(f"/api/v1/ws/takeover/{chat_id}") as ws:
        # 1. Test ping-pong
        print("Testing ping-pong...")
        ws.send_json({"type": "ping"})
        data = ws.receive_json()
        assert data["type"] == "pong"
        assert data["chat_id"] == chat_id
        print("-> Ping-pong: PASSED")

        # 2. Test takeover_start
        print("Testing takeover_start...")
        # Send takeover_start with 2 seconds duration for fast testing
        ws.send_json({"type": "takeover_start", "duration": 2})
        data = ws.receive_json()
        assert data["type"] == "takeover_started"
        assert data["chat_id"] == chat_id
        assert data["duration"] == 2
        print("-> Takeover start event: PASSED")

        # Verify DB is updated to manual
        async def verify_db_mode(expected_mode):
            async with SessionLocal() as db:
                from sqlalchemy import select
                result = await db.execute(
                    select(Interaction).where(Interaction.external_user_id == chat_id)
                )
                interaction = result.scalars().first()
                assert interaction is not None
                assert interaction.mode == expected_mode

        loop.run_until_complete(verify_db_mode("manual"))
        print("-> Database updated to manual: PASSED")

        # 3. Test takeover_end (Manual cancel)
        print("Testing takeover_end (manual cancel)...")
        ws.send_json({"type": "takeover_end"})
        data = ws.receive_json()
        assert data["type"] == "takeover_ended"
        assert data["chat_id"] == chat_id
        
        loop.run_until_complete(verify_db_mode("sora"))
        print("-> Takeover manual end (cancel): PASSED")

        # 4. Test takeover expiration (timer)
        print("Testing takeover automatic expiration...")
        # Start a new takeover with 1 second duration
        ws.send_json({"type": "takeover_start", "duration": 1})
        data = ws.receive_json()
        assert data["type"] == "takeover_started"

        # Wait for the timer on the backend to trigger expiration (1.5 seconds to be safe)
        time.sleep(1.5)

        # The backend should broadcast takeover_expired
        data = ws.receive_json()
        assert data["type"] == "takeover_expired"
        assert data["chat_id"] == chat_id

        # Verify DB is reset to sora
        loop.run_until_complete(verify_db_mode("sora"))
        print("-> Takeover automatic expiration: PASSED")

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
    test_websocket_flow()
    print("All WebSocket verification tests PASSED successfully!")
