from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import redis.asyncio as aioredis
from typing import Dict, Any

from app.core.config import settings
from app.core.database import get_db

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=Dict[str, Any])
async def health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    health_status: Dict[str, Any] = {
        "status": "healthy",
        "services": {
            "api": "online",
            "database": "offline",
            "redis": "offline"
        }
    }
    
    # Check Database connection
    try:
        await db.execute(text("SELECT 1"))
        health_status["services"]["database"] = "online"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["services"]["database"] = f"error: {str(e)}"
        
    # Check Redis connection
    try:
        redis_client = aioredis.from_url(settings.CELERY_BROKER_URL)
        ping_result = await redis_client.ping()
        if ping_result:
            health_status["services"]["redis"] = "online"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["services"]["redis"] = f"error: {str(e)}"
        
    return health_status

@app.get("/")
def read_root():
    return {"message": "Welcome to VIRA Automated Agent API. Go to /docs for Swagger documentation."}
