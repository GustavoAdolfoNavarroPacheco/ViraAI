import datetime
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.database import get_db
from app.domain.models import Channel
from app.infrastructure.social_services import SocialService

router = APIRouter(
    prefix="/channels",
    tags=["channels-oauth"]
)

@router.get("/connect/{platform}")
async def connect_channel(platform: str, state: str = "state"):
    """
    Initiates OAuth 2.0 flow for the specified platform by redirecting the user.
    """
    try:
        auth_url = SocialService.get_auth_url(platform, state)
        return RedirectResponse(url=auth_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/callback/{platform}")
async def oauth_callback(platform: str, code: str, state: str = None, db: AsyncSession = Depends(get_db)):
    """
    Handles OAuth 2.0 callback, exchanges code for tokens, persists in DB,
    and redirects the user back to the frontend.
    """
    try:
        # Exchange code for token details
        token_data = SocialService.exchange_code_for_tokens(platform, code)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth exchange failed: {str(e)}")

    # Calculate token expiration
    expires_in = token_data.get("expires_in", 3600)
    token_expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expires_in)

    # Search for an existing channel for this platform & profile name
    result = await db.execute(
        select(Channel).where(
            Channel.platform == platform,
            Channel.name == token_data["name"]
        )
    )
    channel = result.scalars().first()

    if channel:
        # Update credentials
        channel.auth_token = token_data["access_token"]
        channel.refresh_token = token_data["refresh_token"]
        channel.token_expires_at = token_expires_at
        channel.profile_url = token_data["profile_url"]
        channel.is_active = True
        print(f"[OAuth Callback] Updated existing channel: {channel.name} on {platform}.")
    else:
        # Create a new channel connection
        channel = Channel(
            platform=platform,
            name=token_data["name"],
            auth_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
            token_expires_at=token_expires_at,
            profile_url=token_data["profile_url"],
            is_active=True
        )
        db.add(channel)
        print(f"[OAuth Callback] Connected new channel: {channel.name} on {platform}.")

    await db.commit()

    # Redirect to frontend channel dashboard page
    redirect_url = f"{settings.FRONTEND_URL}/dashboard?connected=true&platform={platform}"
    return RedirectResponse(url=redirect_url)
