"""
Chat API routes for the RAG chatbot service.

This module provides the chat endpoints for question-answering.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import logging

from src.core.embeddings import EmbeddingsClient
from src.core.retrieval import QdrantRetriever
from src.core.llm import LLMClient

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

# Initialize clients (these should be injected via dependency injection in production)
embeddings_client = None
retriever = None
llm_client = None


def initialize_clients(embed_client, qdrant_client, llm_cli):
    """Initialize the route handlers with service clients."""
    global embeddings_client, retriever, llm_client
    embeddings_client = embed_client
    retriever = qdrant_client
    llm_client = llm_cli


# Request/Response Models
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=1000)
    selected_text: Optional[str] = Field(None, max_length=5000)
    language: str = Field("en", regex="^(en|ur)$")

    @validator('question')
    def question_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Question cannot be empty')
        return v


class SourceReference(BaseModel):
    chapter_id: str
    chapter_title: str
    section_id: str
    section_title: str
    url: str


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceReference]
    language: str
    out_of_scope: bool = False
    suggested_chapters: Optional[List[str]] = None


@router.post("/question", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    """
    Ask a question about the textbook content.

    Returns an AI-generated answer based on retrieved textbook content.
    """
    if not embeddings_client or not retriever or not llm_client:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service not initialized"
        )

    try:
        language = request.language

        # Handle selected text context
        if request.selected_text:
            context_chunks = [{
                'content': request.selected_text,
                'section_title': 'Selected Text',
                'chapter_id': 'unknown',
                'section_id': 'selected'
            }]
        else:
            # Search Qdrant
            query_embedding = embeddings_client.embed_query(request.question)
            context_chunks = retriever.search(
                query_vector=query_embedding,
                language=language,
                limit=5,
                score_threshold=0.5
            )

        # Check for no results
        if not context_chunks:
            return ChatResponse(
                answer="I couldn't find relevant information in the textbook to answer your question.",
                sources=[],
                language=language,
                out_of_scope=True,
                suggested_chapters=["chapter-01-foundations"]
            )

        # Generate answer
        answer = llm_client.generate_response(
            question=request.question,
            context_chunks=context_chunks,
            language=language
        )

        # Build sources
        sources = []
        for chunk in context_chunks:
            chapter_id = chunk.get('chapter_id', '')
            sources.append(SourceReference(
                chapter_id=chapter_id,
                chapter_title=_format_chapter_title(chapter_id),
                section_id=chunk.get('section_id', ''),
                section_title=chunk.get('section_title', ''),
                url=f"/{language}/docs/{chapter_id}#{chunk.get('section_id', '')}"
            ))

        return ChatResponse(
            answer=answer,
            sources=sources,
            language=language,
            out_of_scope=False
        )

    except Exception as e:
        logger.error(f"Error in ask_question: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process question"
        )


def _format_chapter_title(chapter_id: str) -> str:
    """Format chapter ID into readable title."""
    titles = {
        'intro': 'Introduction',
        'chapter-01-foundations': 'Physical AI Foundations',
        'chapter-02-ros2': 'ROS 2',
        'chapter-03-gazebo': 'Gazebo & Digital Twins',
        'chapter-04-isaac': 'NVIDIA Isaac',
        'chapter-05-vla': 'Vision-Language-Action Models',
        'chapter-06-capstone': 'Capstone Project'
    }
    return titles.get(chapter_id, chapter_id.replace('-', ' ').title())
