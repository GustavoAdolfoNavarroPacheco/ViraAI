from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import redis.asyncio as aioredis
from typing import Dict, Any

from app.core.config import settings
from app.core.database import get_db
from app.infrastructure.routers.data_routes import router as data_router
from app.infrastructure.routers.rag_routes import router as rag_router
from app.infrastructure.routers.agent_routes import router as agent_router
from app.infrastructure.routers.ws_routes import router as ws_router
from app.infrastructure.routers.oauth_routes import router as oauth_router
from app.infrastructure.routers.post_routes import router as post_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Register routers
app.include_router(data_router, prefix=settings.API_V1_STR)
app.include_router(rag_router, prefix=settings.API_V1_STR)
app.include_router(agent_router, prefix=settings.API_V1_STR)
app.include_router(ws_router, prefix=settings.API_V1_STR)
app.include_router(oauth_router, prefix=settings.API_V1_STR)
app.include_router(post_router, prefix=settings.API_V1_STR)



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
