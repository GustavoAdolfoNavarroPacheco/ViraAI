import asyncio
from app.application.vira_agent import ViraAgent
from app.application.document_processor import DocumentProcessor
from app.infrastructure.rag_service import rag_service

async def run_tests():
    # 1. Test generate_post for Twitter (Mock or real)
    tweet = await ViraAgent.generate_post(
        brand_voice="Tecnológico y Disruptivo",
        topic="Lanzamiento de la plataforma VIRA",
        platform="twitter"
    )
    
    assert tweet
    assert "[Mock Tweet" in tweet or len(tweet) <= 280
    assert "VIRA" in tweet

    # 2. Test generate_post for LinkedIn (Mock or real)
    linkedin_post = await ViraAgent.generate_post(
        brand_voice="Profesional y Educativo",
        topic="Arquitectura Hexagonal con FastAPI",
        platform="linkedin"
    )
    
    assert linkedin_post
    assert "[Mock LinkedIn" in linkedin_post or "#" in linkedin_post

    # 3. Test generate_interaction_reply with RAG context
    # Let's index a mock chunk first to make sure there is content in Qdrant/Mock DB
    mock_vector = [0.1] * 768
    rag_service.index_chunks([{
        "id": 12345,
        "vector": mock_vector,
        "payload": {
            "document_id": 1,
            "filename": "manual_empresa.pdf",
            "chunk_index": 0,
            "content": "VIRA tiene soporte nativo para automatización de publicaciones en Instagram, Twitter y LinkedIn.",
            "synthesis": "Soporte de canales de VIRA."
        }
    }])

    reply = await ViraAgent.generate_interaction_reply(
        interaction_message="¿Qué canales soporta VIRA?",
        history=[],
        platform="whatsapp"
    )
    
    assert reply
    assert "Instagram" in reply or "Twitter" in reply or "LinkedIn" in reply

if __name__ == "__main__":
    asyncio.run(run_tests())
    print("test_vira_agent PASSED successfully!")
