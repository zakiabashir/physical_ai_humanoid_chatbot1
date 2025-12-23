"""
Qdrant client wrapper for vector search and retrieval.
"""

from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter,
    PointIdsList,
    RecommendRequest,
    RecommendResponse,
    SearchRequest,
    SearchResponse,
)
import os


class QdrantRetriever:
    """Wrapper for Qdrant vector database operations."""

    def __init__(
        self,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        collection_en: str = "textbook_en",
        collection_ur: str = "textbook_ur"
    ):
        """
        Initialize Qdrant retriever.

        Args:
            url: Qdrant server URL
            api_key: Qdrant API key (for Qdrant Cloud)
            collection_en: English content collection name
            collection_ur: Urdu content collection name
        """
        self.url = url or os.getenv("QDRANT_URL", "http://localhost:6333")
        self.api_key = api_key or os.getenv("QDRANT_API_KEY")
        self.collection_en = collection_en
        self.collection_ur = collection_ur

        self.client = QdrantClient(url=self.url, api_key=self.api_key)

    def search(
        self,
        query_vector: List[float],
        language: str = "en",
        limit: int = 5,
        score_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar content chunks.

        Args:
            query_vector: Query embedding vector
            language: Language code ('en' or 'ur')
            limit: Maximum number of results
            score_threshold: Minimum similarity score (0-1)

        Returns:
            List of search results with payload
        """
        collection = self.collection_en if language == "en" else self.collection_ur

        try:
            response = self.client.search(
                collection_name=collection,
                query_vector=query_vector,
                limit=limit,
                score_threshold=score_threshold
            )

            results = []
            for hit in response:
                results.append({
                    'score': hit.score,
                    'chapter_id': hit.payload.get('chapter_id'),
                    'section_id': hit.payload.get('section_id'),
                    'section_title': hit.payload.get('section_title'),
                    'content': hit.payload.get('content'),
                    'language': hit.payload.get('language', language)
                })

            return results

        except Exception as e:
            print(f"Search error: {e}")
            return []

    def get_collections(self) -> List[str]:
        """Get list of available collections."""
        collections = self.client.get_collections().collections
        return [c.name for c in collections]

    def collection_exists(self, collection_name: str) -> bool:
        """Check if collection exists."""
        return collection_name in self.get_collections()

    def get_collection_info(self, collection_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a collection."""
        try:
            info = self.client.get_collection(collection_name)
            return {
                'name': collection_name,
                'vectors_count': info.vectors_count,
                'points_count': info.points_count,
                'status': info.status
            }
        except Exception as e:
            print(f"Error getting collection info: {e}")
            return None

    def health_check(self) -> bool:
        """Check if Qdrant is accessible."""
        try:
            collections = self.client.get_collections()
            return True
        except Exception as e:
            print(f"Qdrant health check failed: {e}")
            return False
