"""
Cohere embeddings client for generating text embeddings.
"""

from typing import List
from cohere import Client as CohereClient
import os


class EmbeddingsClient:
    """Client for generating embeddings using Cohere API."""

    def __init__(self, api_key: str = None):
        """
        Initialize Cohere embeddings client.

        Args:
            api_key: Cohere API key (defaults to COHERE_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("Cohere API key must be provided")

        self.client = CohereClient(self.api_key)
        self.model = "embed-multilingual-v3.0"

    def embed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a single query text.

        Args:
            text: Query text to embed

        Returns:
            Embedding vector (list of floats)
        """
        response = self.client.embed(
            texts=[text],
            model=self.model,
            input_type='search_query'
        )
        return response.embeddings[0]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple document texts.

        Args:
            texts: List of document texts to embed

        Returns:
            List of embedding vectors
        """
        response = self.client.embed(
            texts=texts,
            model=self.model,
            input_type='search_document'
        )
        return response.embeddings

    def get_embedding_dimension(self) -> int:
        """Get the dimension of the embedding vectors."""
        # Cohere embed-multilingual-v3.0 returns 1024-dimensional vectors
        return 1024

    def health_check(self) -> bool:
        """Check if Cohere API is accessible."""
        try:
            response = self.client.embed(
                texts=["test"],
                model=self.model,
                input_type='search_query'
            )
            return len(response.embeddings[0]) > 0
        except Exception as e:
            print(f"Cohere health check failed: {e}")
            return False
