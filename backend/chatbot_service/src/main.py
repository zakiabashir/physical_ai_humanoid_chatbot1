"""
RAG Chatbot Service - Main FastAPI application

This service provides question-answering about textbook content
using Retrieval-Augmented Generation (RAG) with Qdrant and Cohere/Groq.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Optional
import logging

from src.core.config import config
from src.core.embeddings import EmbeddingsClient
from src.core.retrieval import QdrantRetriever
from src.core.llm import LLMClient

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Chatbot Service API",
    description="RAG-based chatbot API for AI-Native Textbook Platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
embeddings_client = EmbeddingsClient(api_key=config.cohere_api_key)
retriever = QdrantRetriever(
    url=config.qdrant_url,
    api_key=config.qdrant_api_key,
    collection_en=config.qdrant_collection_en,
    collection_ur=config.qdrant_collection_ur
)
llm_client = LLMClient(api_key=config.groq_api_key, model=config.groq_model)


# Request/Response Models
class ChatRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=1000, description="User's question")
    selected_text: Optional[str] = Field(None, max_length=5000, description="Optional selected text context")
    language: str = Field("en", regex="^(en|ur)$", description="Response language")

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


class HealthResponse(BaseModel):
    status: str
    qdrant: str


# API Routes
@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """
    Health check endpoint.

    Verifies connectivity to Qdrant and returns service status.
    """
    qdrant_status = "connected" if retriever.health_check() else "disconnected"

    return HealthResponse(
        status="ok" if qdrant_status == "connected" else "degraded",
        qdrant=qdrant_status
    )


@app.post("/chat/question", response_model=ChatResponse, tags=["chat"])
async def ask_question(request: ChatRequest):
    """
    Ask a question about the textbook content.

    Processes the question using RAG:
    1. Embed the question using Cohere
    2. Retrieve relevant content from Qdrant
    3. Generate answer using Groq LLM
    4. Return answer with source references
    """
    try:
        # Detect language from question (simple check)
        # TODO: Use better language detection
        language = request.language

        # If selected_text is provided, use it as context
        # Otherwise, search Qdrant
        if request.selected_text:
            context_chunks = [{
                'content': request.selected_text,
                'section_title': 'Selected Text',
                'chapter_id': 'unknown',
                'section_id': 'selected'
            }]
        else:
            # Generate query embedding
            query_embedding = embeddings_client.embed_query(request.question)

            # Search Qdrant for relevant content
            context_chunks = retriever.search(
                query_vector=query_embedding,
                language=language,
                limit=config.max_context_chunks,
                score_threshold=config.min_similarity_score
            )

        # Check if we found relevant content
        if not context_chunks:
            return ChatResponse(
                answer="I couldn't find relevant information in the textbook to answer your question. Try rephrasing or browse the chapters directly." if language == "en" else "میں textbook میں آپ کے سوال کا جواب دینے کے لیے متعلقہ معلومات نہیں مل سکا۔ اپنے سوال کو دوبارہ لکھنے کی کوشش کریں یا براہ راست ابواب دیکھیں۔",
                sources=[],
                language=language,
                out_of_scope=True,
                suggested_chapters=["chapter-01-foundations"]
            )

        # Generate answer using LLM
        answer = llm_client.generate_response(
            question=request.question,
            context_chunks=context_chunks,
            language=language
        )

        # Build source references
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
        logger.error(f"Error processing question: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process question"
        )


@app.get("/chat/streams", tags=["chat"])
async def ask_question_stream(request: ChatRequest):
    """
    Ask a question with streaming response (Server-Sent Events).

    Returns a streaming response for real-time answer generation.
    """
    from fastapi.responses import StreamingResponse

    language = request.language

    # If selected_text is provided, use it as context
    if request.selected_text:
        context_chunks = [{
            'content': request.selected_text,
            'section_title': 'Selected Text',
            'chapter_id': 'unknown',
            'section_id': 'selected'
        }]
    else:
        # Generate query embedding
        query_embedding = embeddings_client.embed_query(request.question)

        # Search Qdrant
        context_chunks = retriever.search(
            query_vector=query_embedding,
            language=language,
            limit=config.max_context_chunks,
            score_threshold=config.min_similarity_score
        )

    if not context_chunks:
        # Return out-of-scope message
        message = "I couldn't find relevant information in the textbook to answer your question." if language == "en" else "میں textbook میں آپ کے سوال کا جواب نہیں مل سکا۔"
        async def generate():
            yield f"data: {message}\n\n"
        return StreamingResponse(generate(), media_type="text/event-stream")

    # Stream LLM response
    async def generate():
        for chunk in llm_client.generate_streaming_response(
            question=request.question,
            context_chunks=context_chunks,
            language=language
        ):
            yield f"data: {chunk}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


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


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting Chatbot Service...")
    logger.info(f"Qdrant URL: {config.qdrant_url}")
    logger.info(f"Cohere Model: {config.cohere_model}")
    logger.info(f"Groq Model: {config.groq_model}")

    # Verify connections
    if retriever.health_check():
        logger.info("Connected to Qdrant")
    else:
        logger.warning("Could not connect to Qdrant")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down Chatbot Service...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.host, port=config.port)
