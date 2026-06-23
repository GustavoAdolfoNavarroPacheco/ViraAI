import logging
from typing import List, Dict, Any, Optional

from app.core.config import settings
from app.infrastructure.rag_service import rag_service

logger = logging.getLogger("ViraAgent")

# Setup GenAI client conditionally
google_genai_client = None
if settings.GEMINI_API_KEY:
    try:
        from google import genai
        google_genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
    except Exception as e:
        logger.error(f"Failed to initialize GenAI Client: {str(e)}")

class ViraAgent:
    @classmethod
    def _generate_mock_post(cls, brand_voice: str, topic: str, platform: str) -> str:
        """
        Generates a mock social media post based on platform constraints.
        """
        platform_lower = platform.lower().strip()
        if "twitter" in platform_lower or "x" in platform_lower:
            return f"🤖 [Mock Tweet - Tono: {brand_voice}] ¿Sabías que la automatización con IA es el futuro del marketing? VIRA te permite programar y generar contenido en segundos sobre: {topic}. ¡Suma valor hoy! #VIRA #Automation"
        elif "linkedin" in platform_lower:
            return (
                f"🤖 [Mock LinkedIn Post - Tono: {brand_voice}]\n\n"
                f"La evolución de la presencia digital hoy exige consistencia y profundidad. "
                f"Hemos estado analizando cómo optimizar estrategias para abordar el tema: '{topic}'.\n\n"
                f"A través de nuestra plataforma automatizada VIRA, integramos agentes de IA (Gemini 3.5 Flash) "
                f"y bases vectoriales para responder interacciones en tiempo real. Esta aproximación modular "
                f"asegura coherencia y velocidad.\n\n"
                f"¿Qué opinas sobre aplicar IA en tus publicaciones?\n\n"
                f"#VIRA #InteligenciaArtificial #Productividad #Marketing"
            )
        else:
            return f"🤖 [Mock Instagram Post - Tono: {brand_voice}] ✨ Ganchos visuales y contenido creativo sobre: {topic}. VIRA automatiza tus redes de forma orgánica y dinámica. 📸 #VIRA #MarketingDigital #Growth"

    @classmethod
    def _generate_mock_reply(cls, message: str, context_chunks: List[Dict[str, Any]], platform: str) -> str:
        """
        Generates a mock interaction reply using RAG context.
        """
        context_str = " | ".join(c["payload"]["content"] for c in context_chunks) if context_chunks else "Sin información relevante."
        return (
            f"🤖 [Mock Reply en {platform.upper()}] Gracias por tu mensaje. "
            f"Respecto a tu consulta, basándome en nuestra base de conocimientos: "
            f"'{context_str}'. Espero que te sea de ayuda. Si tienes otra pregunta, ¡escríbeme!"
        )

    @classmethod
    async def generate_post(cls, brand_voice: str, topic: str, platform: str) -> str:
        """
        Generates a post for a platform with a specific brand voice.
        Includes a Self-Correction Loop / Critic block.
        """
        platform_lower = platform.lower().strip()
        
        # 1. Platform specific instructions
        if "twitter" in platform_lower or "x" in platform_lower:
            platform_rules = "Genera un tweet. Máximo 280 caracteres. Sé directo, conciso e incluye hashtags relevantes al final."
        elif "linkedin" in platform_lower:
            platform_rules = "Genera un post profesional para LinkedIn. Estructurado por párrafos cortos, usa viñetas si es relevante, tono corporativo e inteligente."
        else:
            platform_rules = "Genera un post de Instagram. Lleno de emojis para hacerlo dinámico, con un gancho inicial fuerte y un bloque de hashtags al final."

        if not google_genai_client:
            logger.info("Gemini API key not found. Returning Mock Post.")
            return cls._generate_mock_post(brand_voice, topic, platform)

        try:
            # 2. Main Generation Prompt
            generation_prompt = (
                f"Actúa como un Copywriter Senior de Redes Sociales.\n"
                f"Reglas de la Plataforma: {platform_rules}\n"
                f"Tono y Voz de la Marca (Brand Voice): {brand_voice}\n"
                f"Tema o Instrucción del Post: {topic}\n\n"
                f"Redacta la propuesta de post:"
            )
            
            response = google_genai_client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=generation_prompt
            )
            initial_post = response.text.strip() if response.text else ""
            
            if not initial_post:
                return cls._generate_mock_post(brand_voice, topic, platform)

            # 3. Self-Correction Loop (Critic Mode)
            critic_prompt = (
                f"Actúa como un Editor Jefe de Publicaciones.\n"
                f"Tu rol es evaluar si el siguiente borrador cumple estrictamente con el tono '{brand_voice}' "
                f"y las reglas de {platform}.\n\n"
                f"Borrador:\n{initial_post}\n\n"
                f"Instrucciones de evaluación:\n"
                f"- Si el borrador es excelente y cumple al 100%, responde únicamente la palabra: APROBADO\n"
                f"- Si detectas problemas de longitud, tono o hashtags, responde con la versión corregida y mejorada directamente sin explicaciones extra."
            )
            
            critic_response = google_genai_client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=critic_prompt
            )
            critic_text = critic_response.text.strip() if critic_response.text else ""

            if critic_text.upper().startswith("APROBADO") or critic_text == "APROBADO":
                logger.info("Post approved on first evaluation.")
                return initial_post
            else:
                logger.info("Post was corrected by the self-critique loop.")
                return critic_text

        except Exception as e:
            logger.error(f"Error in Gemini post generation: {str(e)}. Falling back to Mock.")
            return cls._generate_mock_post(brand_voice, topic, platform)

    @classmethod
    async def generate_interaction_reply(cls, interaction_message: str, history: List[Dict[str, str]], platform: str) -> str:
        """
        Generates an automated response to DMs/Comments using RAG.
        """
        # 1. Query vector DB to fetch relevant context
        query_vector = await DocumentProcessor_embedding_mock(interaction_message)
        context_hits = rag_service.query_similarity(query_vector, top_k=2)
        
        # Format context
        context_str = ""
        if context_hits:
            context_str = "\n".join(f"- {hit['payload']['content']}" for hit in context_hits)
            
        if not google_genai_client:
            logger.info("Gemini API key not found. Returning Mock Interaction Reply.")
            return cls._generate_mock_reply(interaction_message, context_hits, platform)

        try:
            # Format history for prompt
            history_str = ""
            for h in history:
                role = "Usuario" if h.get("role") == "user" else "Agente (Tú)"
                history_str += f"{role}: {h.get('content')}\n"

            # 2. Main Response Prompt
            reply_prompt = (
                f"Actúa como el Asistente Virtual Automatizado de la marca en {platform}.\n"
                f"Usa la siguiente información corporativa oficial (Contexto RAG) para responder la pregunta del usuario:\n"
                f"{context_str}\n\n"
                f"Historial de Chat:\n"
                f"{history_str}\n"
                f"Mensaje nuevo del Usuario:\n"
                f"{interaction_message}\n\n"
                f"Instrucciones:\n"
                f"- Responde de manera concisa y educada.\n"
                f"- Limítate estrictamente a la información proveída en el Contexto RAG. "
                f"Si la información no es suficiente para responder, dilo de forma amable pero profesional.\n"
                f"- No inventes datos.\n\n"
                f"Respuesta:"
            )
            
            response = google_genai_client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=reply_prompt
            )
            return response.text.strip() if response.text else "Disculpa, no pude procesar una respuesta en este momento."

        except Exception as e:
            logger.error(f"Error in Gemini interaction reply: {str(e)}. Falling back to Mock.")
            return cls._generate_mock_reply(interaction_message, context_hits, platform)

# Inline helper to avoid circular imports of DocumentProcessor
async def DocumentProcessor_embedding_mock(text: str) -> List[float]:
    from app.application.document_processor import DocumentProcessor
    return await DocumentProcessor.get_embedding(text)
