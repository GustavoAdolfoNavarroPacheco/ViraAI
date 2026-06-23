from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List
import random

from app.core.database import get_db
from app.domain.models import KnowledgeBase
from app.application.document_processor import DocumentProcessor
from app.infrastructure.rag_service import rag_service

router = APIRouter(
    prefix="/rag",
    tags=["rag-knowledge-base"]
)

@router.post("/upload-document", response_model=Dict[str, Any])
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Sube un archivo PDF de base de conocimiento, extrae su texto, realiza chunking semántico,
    sintetiza el contenido usando Gemini 3.5 Flash, calcula embeddings e indexa en Qdrant.
    También persiste los metadatos y síntesis en PostgreSQL.
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Solo se admiten documentos en formato PDF."
        )

    try:
        content = await file.read()
        
        # 1. Persist initial metadata in PostgreSQL
        # We save filepath as a reference
        db_doc = KnowledgeBase(
            filename=file.filename,
            filepath=f"knowledge_store/{file.filename}",
            summary="Procesando..."
        )
        db.add(db_doc)
        await db.commit()
        await db.refresh(db_doc)
        
        # 2. Process chunks and upload vectors to Qdrant
        num_chunks, doc_summary = await DocumentProcessor.process_and_index_document(
            filename=file.filename,
            file_content=content,
            document_id=db_doc.id
        )
        
        # 3. Update PostgreSQL with the final synthesis/summary
        db_doc.summary = doc_summary
        await db.commit()
        await db.refresh(db_doc)
        
        return {
            "success": True,
            "document_id": db_doc.id,
            "filename": db_doc.filename,
            "chunks_indexed": num_chunks,
            "summary": doc_summary,
            "created_at": db_doc.created_at
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en el procesamiento del documento RAG: {str(e)}"
        )

@router.post("/query", response_model=Dict[str, Any])
async def query_knowledge_base(
    payload: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Realiza una búsqueda semántica de información en la base de datos vectorial Qdrant.
    Payload: {"query": "pregunta del usuario", "top_k": 4}
    """
    query = payload.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="Debe proveer una consulta en el parámetro 'query'.")
        
    top_k = payload.get("top_k", 4)
    
    try:
        # 1. Get embedding of query
        query_vector = await DocumentProcessor.get_embedding(query)
        
        # 2. Query Qdrant
        matches = rag_service.query_similarity(query_vector, top_k=top_k)
        
        return {
            "success": True,
            "query": query,
            "results": matches
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en la consulta semántica: {str(e)}"
        )
