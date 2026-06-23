import logging
import math
from typing import List, Dict, Any, Optional

logger = logging.getLogger("RAGService")

# Try to import qdrant_client, catch DLL/AppLocker errors (e.g., numpy loading issues)
try:
    from qdrant_client import QdrantClient
    from qdrant_client.http.models import PointStruct, Distance, VectorParams
    QDRANT_AVAILABLE = True
except (ImportError, Exception) as e:
    logger.warning(f"QdrantClient is not available. Falling back to pure Python Mock Vector DB. Reason: {str(e)}")
    QDRANT_AVAILABLE = False

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """
    Computes cosine similarity between two vectors using pure Python.
    """
    if len(v1) != len(v2):
        return 0.0
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_a = math.sqrt(sum(a * a for a in v1))
    norm_b = math.sqrt(sum(b * b for b in v2))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot_product / (norm_a * norm_b)

class PurePythonVectorDB:
    """
    A lightweight, pure Python in-memory vector database mock.
    Calculates cosine similarity mathematically without numpy or Qdrant dependencies.
    """
    def __init__(self):
        self.collections: Dict[str, List[Dict[str, Any]]] = {}

    def ensure_collection(self, name: str):
        if name not in self.collections:
            self.collections[name] = []

    def upsert(self, collection_name: str, points: List[Dict[str, Any]]):
        self.ensure_collection(collection_name)
        existing_ids = {p["id"]: idx for idx, p in enumerate(self.collections[collection_name])}
        
        for point in points:
            pid = point["id"]
            if pid in existing_ids:
                # Update
                self.collections[collection_name][existing_ids[pid]] = point
            else:
                # Insert
                self.collections[collection_name].append(point)

    def search(self, collection_name: str, query_vector: List[float], limit: int) -> List[Any]:
        self.ensure_collection(collection_name)
        
        scored_hits = []
        for point in self.collections[collection_name]:
            sim = cosine_similarity(query_vector, point["vector"])
            # Mock hit object
            class Hit:
                def __init__(self, id, score, payload):
                    self.id = id
                    self.score = score
                    self.payload = payload
            scored_hits.append(Hit(point["id"], sim, point["payload"]))
            
        # Sort by score descending
        scored_hits.sort(key=lambda x: x.score, reverse=True)
        return scored_hits[:limit]

class RAGService:
    def __init__(self):
        self.default_collection = "vira_knowledge_base"
        self.vector_size = 768
        
        if QDRANT_AVAILABLE:
            from app.core.config import settings
            if settings.QDRANT_IN_MEMORY:
                logger.info("Initializing QdrantClient IN-MEMORY mode.")
                self.client = QdrantClient(":memory:")
            else:
                logger.info(f"Connecting to QdrantClient at {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
                self.client = QdrantClient(
                    host=settings.QDRANT_HOST,
                    port=settings.QDRANT_PORT
                )
            self.mock_db = None
        else:
            logger.info("Initializing PurePythonVectorDB in-memory mock database.")
            self.client = None
            self.mock_db = PurePythonVectorDB()

    def ensure_collection(self, collection_name: Optional[str] = None) -> str:
        col_name = collection_name or self.default_collection
        if QDRANT_AVAILABLE and self.client:
            try:
                collections = self.client.get_collections().collections
                exists = any(c.name == col_name for c in collections)
                
                if not exists:
                    logger.info(f"Creating collection '{col_name}' in Qdrant...")
                    self.client.create_collection(
                        collection_name=col_name,
                        vectors_config=VectorParams(
                            size=self.vector_size,
                            distance=Distance.COSINE
                        )
                    )
                return col_name
            except Exception as e:
                logger.error(f"Failed to ensure collection '{col_name}': {str(e)}")
                raise
        else:
            if self.mock_db:
                self.mock_db.ensure_collection(col_name)
            return col_name

    def index_chunks(self, chunks: List[Dict[str, Any]], collection_name: Optional[str] = None):
        col_name = self.ensure_collection(collection_name)
        
        if QDRANT_AVAILABLE and self.client:
            points = []
            for idx, chunk in enumerate(chunks):
                points.append(
                    PointStruct(
                        id=chunk.get("id", idx),
                        vector=chunk["vector"],
                        payload=chunk["payload"]
                    )
                )
            try:
                self.client.upsert(collection_name=col_name, points=points)
                logger.info(f"Indexed {len(points)} chunks into Qdrant collection '{col_name}'")
            except Exception as e:
                logger.error(f"Qdrant upsert failed: {str(e)}")
                raise
        else:
            # Fallback mock upsert
            if self.mock_db:
                self.mock_db.upsert(col_name, chunks)
                logger.info(f"[MOCK] Indexed {len(chunks)} chunks into Mock collection '{col_name}'")

    def query_similarity(self, query_vector: List[float], top_k: int = 4, collection_name: Optional[str] = None) -> List[Dict[str, Any]]:
        col_name = self.ensure_collection(collection_name)
        
        if QDRANT_AVAILABLE and self.client:
            try:
                search_result = self.client.search(
                    collection_name=col_name,
                    query_vector=query_vector,
                    limit=top_k
                )
                results = []
                for hit in search_result:
                    results.append({
                        "id": hit.id,
                        "score": hit.score,
                        "payload": hit.payload
                    })
                return results
            except Exception as e:
                logger.error(f"Qdrant query failed: {str(e)}")
                return []
        else:
            # Fallback mock query
            if self.mock_db:
                hits = self.mock_db.search(col_name, query_vector, limit=top_k)
                results = []
                for hit in hits:
                    results.append({
                        "id": hit.id,
                        "score": hit.score,
                        "payload": hit.payload
                    })
                return results
            return []

# Singleton instance
rag_service = RAGService()
