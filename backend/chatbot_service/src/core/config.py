"""
Configuration settings for chatbot service.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class ChatbotConfig(BaseSettings):
    """Configuration for RAG chatbot service."""

    # Qdrant Configuration
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: Optional[str] = None
    qdrant_collection_en: str = "textbook_en"
    qdrant_collection_ur: str = "textbook_ur"

    # Cohere Configuration
    cohere_api_key: str
    cohere_model: str = "embed-multilingual-v3.0"

    # Groq Configuration
    groq_api_key: str
    groq_model: str = "llama-3.1-70b-versatile"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8002

    # RAG Configuration
    max_context_chunks: int = 5
    min_similarity_score: float = 0.5
    max_tokens: int = 2000

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global config instance
config = ChatbotConfig()
