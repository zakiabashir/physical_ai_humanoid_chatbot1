"""
LLM client for generating chatbot responses using Groq API.
"""

from typing import List, Dict, Any, Optional
from groq import Groq
import os


class LLMClient:
    """Client for generating responses using Groq LLM API."""

    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize Groq LLM client.

        Args:
            api_key: Groq API key (defaults to GROQ_API_KEY env var)
            model: Model name (defaults to llama-3.1-70b-versatile)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("Groq API key must be provided")

        self.model = model or os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")
        self.client = Groq(api_key=self.api_key)

    def generate_response(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]],
        language: str = "en",
        max_tokens: int = 1000
    ) -> str:
        """
        Generate answer to question based on retrieved context.

        Args:
            question: User's question
            context_chunks: Retrieved content chunks
            language: Response language ('en' or 'ur')
            max_tokens: Maximum tokens in response

        Returns:
            Generated answer text
        """
        # Build context from chunks
        context_text = self._build_context(context_chunks)

        # Build prompt
        system_prompt = self._get_system_prompt(language)
        user_prompt = self._build_user_prompt(question, context_text, language)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.3  # Lower temperature for more factual responses
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error generating response: {str(e)}"

    def _build_context(self, chunks: List[Dict[str, Any]]) -> str:
        """Build context text from retrieved chunks."""
        context_parts = []

        for i, chunk in enumerate(chunks):
            section_title = chunk.get('section_title', 'Unknown Section')
            content = chunk.get('content', '')
            context_parts.append(f"[Section {i+1}: {section_title}]\n{content}")

        return "\n\n---\n\n".join(context_parts)

    def _get_system_prompt(self, language: str) -> str:
        """Get system prompt for the LLM."""
        if language == "ur":
            return """آپ ایک AI معلم ہیں جو فزیکل AI اور انسان نما روبوٹکس کے بارے میں ایک نصابی کتاب کے مبنی پر سوالات کے جواب دیتے ہیں۔

ہدایات:
1. دی گئی متن سے جواب دیں
2. اگر متن میں جواب نہیں ہے، تو کہیں کہ یہ کتاب میں شامل نہیں ہے
2. جواب واضح اور مختصر رکھیں
4. مناسب کورڈ مثالز شامل کریں اگر ممکن ہو
5. زبان: اردو"""
        else:
            return """You are an AI tutor helping students learn Physical AI and Humanoid Robotics from a textbook.

Instructions:
1. Answer ONLY using the provided textbook content
2. If the answer is not in the context, state that the topic is not covered in this textbook
3. Provide clear, concise answers
4. Include relevant code examples if appropriate
5. Cite the specific sections you're referencing
6. Language: English"""

    def _build_user_prompt(
        self,
        question: str,
        context: str,
        language: str
    ) -> str:
        """Build user prompt with question and context."""
        if language == "ur":
            return f"""درج ذیل متن کا استعمال کرتے ہوئے اس سوال کا جواب دیں:

**متن:**
{context}

**سوال:**
{question}

جواب:"""
        else:
            return f"""Using the following textbook content, answer the question:

**Textbook Content:**
{context}

**Question:**
{question}

Answer:"""

    def generate_streaming_response(
        self,
        question: str,
        context_chunks: List[Dict[str, Any]],
        language: str = "en"
    ):
        """
        Generate streaming response using Server-Sent Events.

        Yields chunks of the response as they're generated.
        """
        context_text = self._build_context(context_chunks)
        system_prompt = self._get_system_prompt(language)
        user_prompt = self._build_user_prompt(question, context_text, language)

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream=True,
                temperature=0.3
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            yield f"Error: {str(e)}"

    def health_check(self) -> bool:
        """Check if Groq API is accessible."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            print(f"Groq health check failed: {e}")
            return False
