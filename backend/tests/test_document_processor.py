import asyncio
from unittest.mock import MagicMock, patch
from app.application.document_processor import DocumentProcessor
from app.infrastructure.rag_service import rag_service

class MockPage:
    def __init__(self, text):
        self.text = text
    def extract_text(self):
        return self.text

class MockPdfReader:
    def __init__(self, stream):
        self.pages = [
            MockPage("VIRA es un agente inteligente para automatización de redes sociales."),
            MockPage("El sistema VIRA permite programar publicaciones en Twitter y LinkedIn."),
            MockPage("El RAG de VIRA almacena conocimiento corporativo y responde interacciones.")
        ]

async def run_tests():
    # 1. Test semantic chunking
    long_text = (
        "Primer párrafo sobre VIRA.\n\n"
        "Segundo párrafo sobre redes sociales.\n\n"
        "Tercer párrafo sobre base vectorial."
    )
    chunks = DocumentProcessor.semantic_chunk_text(long_text, max_chunk_size=100)
    assert len(chunks) == 2
    assert chunks[0] == "Primer párrafo sobre VIRA.\n\nSegundo párrafo sobre redes sociales."
    
    # 2. Test mock embedding generation
    emb = await DocumentProcessor.get_embedding("Test text")
    assert len(emb) == 768
    assert isinstance(emb, list)
    assert isinstance(emb[0], float)

    # 3. Test full document process and index to Qdrant (in-memory)
    # We patch pypdf.PdfReader to use our MockPdfReader
    with patch("pypdf.PdfReader", new=MockPdfReader):
        dummy_pdf_bytes = b"%PDF-1.4 dummy contents"
        num_chunks, summary = await DocumentProcessor.process_and_index_document(
            filename="manual_vira.pdf",
            file_content=dummy_pdf_bytes,
            document_id=999
        )
        
        assert num_chunks == 1
        assert "manual_vira.pdf" in summary or "[Síntesis Simulada]" in summary

        # 4. Query similarity search from Qdrant
        query_vector = await DocumentProcessor.get_embedding("RAG y base vectorial")
        matches = rag_service.query_similarity(query_vector, top_k=2)
        
        assert len(matches) == 1
        # Check payload fields
        assert "content" in matches[0]["payload"]
        assert "filename" in matches[0]["payload"]
        assert matches[0]["payload"]["filename"] == "manual_vira.pdf"
        assert matches[0]["payload"]["document_id"] == 999

if __name__ == "__main__":
    asyncio.run(run_tests())
    print("test_document_processor PASSED successfully!")
