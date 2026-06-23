import datetime
from typing import Optional
from pydantic import BaseModel

# --- Channel Schemas ---
class ChannelBase(BaseModel):
    platform: str
    name: str
    profile_url: Optional[str] = None
    is_active: bool = True

class ChannelResponse(ChannelBase):
    id: int

    model_config = {
        "from_attributes": True
    }

# --- Post Schemas ---
class PostBase(BaseModel):
    channel_id: int
    content: str
    media_url: Optional[str] = None
    scheduled_for: Optional[datetime.datetime] = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    content: Optional[str] = None
    media_url: Optional[str] = None
    status: Optional[str] = None
    scheduled_for: Optional[datetime.datetime] = None

class PostResponse(PostBase):
    id: int
    status: str
    published_at: Optional[datetime.datetime] = None
    engagement_rate: float
    impressions: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = {
        "from_attributes": True
    }
