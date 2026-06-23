import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, ForeignKey, Text, Float, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="recruiter") # admin, recruiter, analyst
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )

class Channel(Base):
    __tablename__ = "channels"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    platform: Mapped[str] = mapped_column(String(50), nullable=False)  # linkedin, twitter, instagram
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    auth_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    refresh_token: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    profile_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="channel", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    media_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="draft")  # draft, review, approved, scheduled, published, failed
    scheduled_for: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    published_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    engagement_rate: Mapped[float] = mapped_column(Float, default=0.0)
    impressions: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )
    
    channel: Mapped["Channel"] = relationship("Channel", back_populates="posts")
    interactions: Mapped[List["Interaction"]] = relationship("Interaction", back_populates="post", cascade="all, delete-orphan")

class Interaction(Base):
    __tablename__ = "interactions"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    post_id: Mapped[Optional[int]] = mapped_column(ForeignKey("posts.id", ondelete="SET NULL"), nullable=True)
    external_user_id: Mapped[str] = mapped_column(String(100), nullable=False)
    external_user_name: Mapped[str] = mapped_column(String(100), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    reply_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    source_platform: Mapped[str] = mapped_column(String(50), nullable=False)  # linkedin, twitter, instagram, whatsapp
    mode: Mapped[str] = mapped_column(String(50), default="sora")  # sora (automatic AI), manual (human takeover)
    takeover_ends_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    post: Mapped[Optional["Post"]] = relationship("Post", back_populates="interactions")

class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    filepath: Mapped[str] = mapped_column(String(255), nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )
