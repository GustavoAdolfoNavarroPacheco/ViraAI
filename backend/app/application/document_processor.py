import io
import hashlib
import random
import logging
from typing import List, Dict, Any, Tuple
import pypdf

from app.core.config import settings
from app.infrastructure.rag_service import rag_service

logger = logging.getLogger("DocumentProcessor")

# Conditional import of google-genai client
google_genai_client = None
if settings.GEMINI_API_KEY:
    try:
        from google import genai
        google_genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
        logger.info("Google GenAI client initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to import or initialize Google GenAI Client: {str(e)}")

class DocumentProcessor:
    @staticmethod
    def extract_text_from_pdf(pdf_bytes: bytes) -> str:
        """
        Extracts plain text from PDF bytes using PyPDF.
        """
        pdf_file = io.BytesIO(pdf_bytes)
        reader = pypdf.PdfReader(pdf_file)
        full_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text.append(text)
        return "\n\n".join(full_text)

    @staticmethod
    def semantic_chunk_text(text: str, max_chunk_size: int = 1000) -> List[str]:
        """
        Splits text by double newlines (paragraphs) and groups them
        until they reach max_chunk_size characters.
        """
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = []
        current_size = 0

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            para_len = len(para)
            if current_size + para_len > max_chunk_size and current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = [para]
                current_size = para_len
            else:
                current_chunk.append(para)
                current_size += para_len + 2  # account for \n\n separator

        if current_chunk:
            chunks.append("\n\n".join(current_chunk))

        return chunks

    @classmethod
    def _generate_mock_embedding(cls, text: str) -> List[float]:
        """
        Generates a deterministic pseudo-random embedding vector of 768 dimensions.
        Used when GEMINI_API_KEY is not provided.
        """
        seed_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        seed = int(seed_hash, 16) % (10**8)
        rng = random.Random(seed)
        return [rng.uniform(-1, 1) for _ in range(768)]

    @classmethod
    def _generate_mock_summary(cls, chunk: str) -> str:
        """
        Generates a mock synthesis of a chunk.
        """
        words = chunk.split()
        summary = f"[Síntesis Simulada] Fragmento de {len(words)} palabras. Temas clave: "
        summary += ", ".join(words[:5]) + "..."
        return summary

    @classmethod
    async def get_embedding(cls, text: str) -> List[float]:
        """
        Gets embedding using Gemini API, or returns a mock vector if API key is missing.
        """
        if google_genai_client:
            try:
                # Call modern Gemini embedding API
                response = google_genai_client.models.embed_content(
                    model="text-embedding-004",
                    contents=text
                )
                return response.embeddings[0].values
            except Exception as e:
                logger.error(f"Error calling Gemini Embedding API: {str(e)}. Falling back to mock.")
                
        return cls._generate_mock_embedding(text)

    @classmethod
    async def synthesize_chunk(cls, chunk: str) -> str:
        """
        Uses Gemini 3.5 Flash to synthesize/summarize the text chunk for better RAG context,
        or returns a mock summary if API key is missing.
        """
        if google_genai_client:
            try:
                prompt = (
                    "Genera una síntesis contextual concisa (máximo 2 oraciones) "
                    "del siguiente fragmento de texto para indexación semántica. "
                    "Resalta los conceptos, entidades y temas principales.\n\n"
                    f"Texto:\n{chunk}\n\n"
                    "Síntesis:"
                )
                response = google_genai_client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=prompt
                )
                if response.text:
                    return response.text.strip()
            except Exception as e:
                logger.error(f"Error calling Gemini Generation API: {str(e)}. Falling back to mock.")

        return cls._generate_mock_summary(chunk)

    @classmethod
    async def process_and_index_document(cls, filename: str, file_content: bytes, document_id: int) -> Tuple[int, str]:
        """
        Processes PDF, chunks it, synthesizes each chunk, gets embeddings, and saves to Qdrant.
        """
        # 1. Extract text
        text = cls.extract_text_from_pdf(file_content)
        if not text.strip():
            raise ValueError("No se pudo extraer texto del documento PDF.")

        # 2. Chunk text
        chunks = cls.semantic_chunk_text(text)
        logger.info(f"Document '{filename}' split into {len(chunks)} chunks.")

        # 3. Process each chunk
        qdrant_chunks = []
        full_summary = []

        for idx, chunk in enumerate(chunks):
            # Synthesize
            synthesis = await cls.synthesize_chunk(chunk)
            full_summary.append(synthesis)

            # Generate embedding on the combined context (synthesis + chunk)
            combined_text = f"Síntesis: {synthesis}\n\nContenido: {chunk}"
            vector = await cls.get_embedding(combined_text)

            # Generate unique point ID (integer or string)
            # Combine document_id and chunk index
            point_id = int(hashlib.md5(f"{document_id}_{idx}".encode()).hexdigest()[:8], 16)

            qdrant_chunks.append({
                "id": point_id,
                "vector": vector,
                "payload": {
                    "document_id": document_id,
                    "filename": filename,
                    "chunk_index": idx,
                    "content": chunk,
                    "synthesis": synthesis
                }
            })

        # 4. Index in Vector DB
        rag_service.index_chunks(qdrant_chunks)

        # Generate a general document summary
        doc_summary = "\n".join(full_summary[:5])  # Take first 5 chunk summaries
        if len(full_summary) > 5:
            doc_summary += "\n[Y más fragmentos...]"

        return len(chunks), doc_summary
