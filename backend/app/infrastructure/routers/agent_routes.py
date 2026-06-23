from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from app.application.vira_agent import ViraAgent

router = APIRouter(
    prefix="/agent",
    tags=["ai-agent-core"]
)

@router.post("/generate-post", response_model=Dict[str, Any])
async def generate_post(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Genera un post de redes sociales optimizado para la plataforma deseada,
    aplicando las reglas de la red social, el tono de voz de la marca,
    y pasando por un ciclo automático de autocrítica y corrección.
    """
    brand_voice = payload.get("brand_voice")
    topic = payload.get("topic")
    platform = payload.get("platform")
    
    if not brand_voice or not topic or not platform:
        raise HTTPException(
            status_code=400,
            detail="Debe suministrar 'brand_voice', 'topic' y 'platform' en el cuerpo de la petición."
        )
        
    try:
        content = await ViraAgent.generate_post(
            brand_voice=brand_voice,
            topic=topic,
            platform=platform
        )
        return {
            "success": True,
            "platform": platform,
            "brand_voice": brand_voice,
            "topic": topic,
            "post_content": content
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la generación de la publicación: {str(e)}"
        )

@router.post("/chat-interaction", response_model=Dict[str, Any])
async def chat_interaction(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Genera una respuesta automática a un comentario o mensaje directo (DM)
    del usuario en base a la información contextual recuperada de la base vectorial (RAG)
    y el historial de conversación.
    """
    message = payload.get("message")
    history = payload.get("history", [])
    platform = payload.get("platform", "whatsapp")
    
    if not message:
        raise HTTPException(
            status_code=400,
            detail="Debe suministrar el parámetro 'message' en la petición."
        )
        
    try:
        reply = await ViraAgent.generate_interaction_reply(
            interaction_message=message,
            history=history,
            platform=platform
        )
        return {
            "success": True,
            "platform": platform,
            "message": message,
            "reply": reply
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar la respuesta de interacción: {str(e)}"
        )
