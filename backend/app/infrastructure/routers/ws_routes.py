import asyncio
import datetime
from typing import Dict
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from app.core.database import SessionLocal
from app.domain.models import Interaction
from app.infrastructure.websocket_manager import manager

router = APIRouter(
    prefix="/ws",
    tags=["websockets-takeover"]
)

# Active timer tasks mapping: chat_id -> asyncio.Task
takeover_tasks: Dict[str, asyncio.Task] = {}

async def db_update_takeover_mode(chat_id: str, mode: str, seconds: int = None):
    """
    Helper to update the takeover mode in the database.
    """
    async with SessionLocal() as db:
        # Check if there is an existing interaction for this external_user_id
        result = await db.execute(
            select(Interaction).where(Interaction.external_user_id == chat_id)
        )
        interaction = result.scalars().first()
        
        takeover_ends_at = None
        if mode == "manual" and seconds:
            takeover_ends_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=seconds)
            
        if interaction:
            interaction.mode = mode
            interaction.takeover_ends_at = takeover_ends_at
        else:
            # Create a mock/placeholder interaction record to track state
            interaction = Interaction(
                external_user_id=chat_id,
                external_user_name=chat_id,
                message="[System Takeover Initialization]",
                reply_content=None,
                source_platform="websocket",
                mode=mode,
                takeover_ends_at=takeover_ends_at
            )
            db.add(interaction)
            
        await db.commit()
        print(f"[WebSocket DB] Updated chat {chat_id} mode to {mode}.")

async def takeover_timer_task(chat_id: str, duration: int):
    """
    Background timer that runs for 'duration' seconds.
    If it completes without cancellation, it returns control to Sora AI (mode='sora')
    and broadcasts a message to the frontend.
    """
    try:
        await asyncio.sleep(duration)
        # Timer expired: return to AI
        await db_update_takeover_mode(chat_id, "sora")
        
        # Broadcast expiration message
        await manager.broadcast_to_chat({
            "type": "takeover_expired",
            "chat_id": chat_id,
            "message": "VIRA IA ha retomado el control automáticamente debido a inactividad."
        }, chat_id)
        
        # Remove task from registry
        if chat_id in takeover_tasks:
            del takeover_tasks[chat_id]
            
        print(f"[WebSocket Timer] Takeover expired for chat {chat_id}. Reverted to sora.")
    except asyncio.CancelledError:
        print(f"[WebSocket Timer] Takeover timer cancelled for chat {chat_id}.")
        raise

@router.websocket("/takeover/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: str):
    await manager.connect(websocket, chat_id)
    try:
        while True:
            # Expect JSON messages from the client
            data = await websocket.receive_json()
            event_type = data.get("type")
            
            if event_type == "takeover_start":
                print(f"[WebSocket] Received takeover_start for chat {chat_id}.")
                # Cancel existing timer task if any
                if chat_id in takeover_tasks:
                    takeover_tasks[chat_id].cancel()
                    
                # Update DB to manual mode
                await db_update_takeover_mode(chat_id, "manual", seconds=300)
                
                # Start new timer (defaults to 300 seconds, custom allowed for testing)
                duration = data.get("duration", 300)
                takeover_tasks[chat_id] = asyncio.create_task(takeover_timer_task(chat_id, duration))
                
                # Broadcast back to all clients in the same chat
                await manager.broadcast_to_chat({
                    "type": "takeover_started",
                    "chat_id": chat_id,
                    "duration": duration,
                    "message": "Control manual activado por el operador."
                }, chat_id)
                
            elif event_type == "takeover_end":
                print(f"[WebSocket] Received takeover_end for chat {chat_id}.")
                # Cancel existing timer task if any
                if chat_id in takeover_tasks:
                    takeover_tasks[chat_id].cancel()
                    del takeover_tasks[chat_id]
                    
                # Update DB to sora mode
                await db_update_takeover_mode(chat_id, "sora")
                
                # Broadcast back
                await manager.broadcast_to_chat({
                    "type": "takeover_ended",
                    "chat_id": chat_id,
                    "message": "El operador ha devuelto el control a VIRA IA."
                }, chat_id)
                
            elif event_type == "ping":
                await websocket.send_json({"type": "pong", "chat_id": chat_id})
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, chat_id)
    except Exception as e:
        print(f"[WebSocket Error] Exception on connection {chat_id}: {e}")
        manager.disconnect(websocket, chat_id)
