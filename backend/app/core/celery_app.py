import redis
from celery import Celery
from app.core.config import settings

# Initialize Celery app
celery_app = Celery(
    "vira_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Celery configurations
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Auto-discover tasks from app.application
celery_app.autodiscover_tasks(["app.application"])

# Resiliency: If Redis is offline, enable eager execution (run tasks synchronously)
try:
    # Use redis.from_url to test connection
    r = redis.from_url(settings.CELERY_BROKER_URL, socket_connect_timeout=2)
    r.ping()
    print("[Celery] Redis connection established. Running in asynchronous mode.")
except Exception as e:
    print(f"[Celery] Redis is offline or timed out: {e}. Falling back to Eager Mode (synchronous task execution).")
    celery_app.conf.update(
        task_always_eager=True,
        task_eager_propagates=True,
    )
