import asyncio
from app.core.database import engine, Base
# Import all models to ensure they are registered on the Base metadata
from app.domain.models import User, Channel, Post, Interaction, KnowledgeBase

async def init_db():
    print("[DB Init] Connecting to database engine...")
    try:
        async with engine.begin() as conn:
            # Create all tables if they do not exist
            await conn.run_sync(Base.metadata.create_all)
        print("[DB Init] All database tables initialized successfully.")
    except Exception as e:
        print(f"[DB Init] Error during database initialization: {e}")
        # Do not raise here so the container startup doesn't crash on temporary postgres lag,
        # but let's let uvicorn handle connection errors later if any.

if __name__ == "__main__":
    asyncio.run(init_db())
