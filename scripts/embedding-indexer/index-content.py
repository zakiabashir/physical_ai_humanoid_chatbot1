"""
Content Indexing Script for RAG Chatbot

This script indexes markdown textbook content into Qdrant vector database
for semantic search and retrieval in the RAG chatbot.
"""

import argparse
import os
import re
import time
from pathlib import Path
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from cohere import Client as CohereClient

# Content chunking configuration
CHUNK_SIZE = 800  # tokens (roughly)
CHUNK_OVERLAP = 100  # tokens


def read_markdown_file(file_path: str) -> str:
    """Read markdown file content."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_sections(content: str, file_path: str) -> List[Dict[str, Any]]:
    """
    Extract sections from markdown content.

    Returns list of dicts with keys: title, content, level, header_id
    """
    lines = content.split('\n')
    sections = []
    current_section = {'title': 'Introduction', 'content': [], 'level': 0, 'header_id': 'intro'}

    for line in lines:
        # Check for headers
        header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if header_match:
            # Save previous section
            if current_section['content']:
                sections.append({
                    **current_section,
                    'content': '\n'.join(current_section['content'])
                })

            # Start new section
            level = len(header_match.group(1))
            title = header_match.group(2).strip()
            header_id = title.lower().replace(' ', '-').replace('/', '-').replace('(', '').replace(')', '')

            current_section = {
                'title': title,
                'content': [],
                'level': level,
                'header_id': header_id
            }
        else:
            current_section['content'].append(line)

    # Add last section
    if current_section['content']:
        sections.append({
            **current_section,
            'content': '\n'.join(current_section['content'])
        })

    return sections


def chunk_text(text: str, max_length: int = 2000) -> List[str]:
    """
    Split text into chunks suitable for embedding.

    Chunks respect paragraph boundaries when possible.
    """
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 > max_length:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para
        else:
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def get_embeddings(texts: List[str], cohere_client: CohereClient) -> List[List[float]]:
    """Get embeddings from Cohere API."""
    response = cohere_client.embed(
        texts=texts,
        model='embed-multilingual-v3.0',
        input_type='search_document'
    )
    return response.embeddings


def index_content(
    content_dir: str,
    collection_name: str,
    language: str,
    qdrant_url: str,
    qdrant_api_key: str,
    cohere_api_key: str
):
    """
    Index markdown content to Qdrant collection.

    Args:
        content_dir: Directory containing markdown files
        collection_name: Name of Qdrant collection
        language: Language code ('en' or 'ur')
        qdrant_url: Qdrant server URL
        qdrant_api_key: Qdrant API key
        cohere_api_key: Cohere API key
    """
    # Initialize clients
    qdrant = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    cohere = CohereClient(cohere_api_key)

    # Get collection info
    collections = qdrant.get_collections().collections
    collection_names = [c.name for c in collections]

    # Create collection if not exists
    if collection_name not in collection_names:
        qdrant.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
        )
        print(f"Created collection: {collection_name}")

    # Process markdown files - collect all chunks first
    md_files = list(Path(content_dir).glob('**/*.md'))

    chunks_to_embed = []  # List of (chunk, metadata) tuples
    point_id = 0

    for md_file in md_files:
        print(f"Processing: {md_file}")

        # Read and extract sections
        content = read_markdown_file(str(md_file))
        sections = extract_sections(content, str(md_file))

        # Get chapter and section info from filename
        chapter_id = md_file.stem.replace('chapter-', '').replace('intro', 'intro')

        for section in sections:
            # Chunk the section content
            chunks = chunk_text(section['content'])

            for chunk_idx, chunk in enumerate(chunks):
                if len(chunk.strip()) < 50:  # Skip very short chunks
                    continue

                chunks_to_embed.append({
                    'chunk': chunk,
                    'metadata': {
                        'chapter_id': chapter_id,
                        'section_id': section['header_id'],
                        'section_title': section['title'],
                        'language': language,
                        'chunk_index': chunk_idx
                    },
                    'point_id': point_id
                })
                point_id += 1

    print(f"Total chunks to embed: {len(chunks_to_embed)}")

    # Process embeddings in batches (Cohere trial limit: 100 calls/min)
    embed_batch_size = 20  # Max 20 texts per call
    api_delay = 0.7  # 700ms delay between batches (safely under 60/min limit)

    points = []
    for i in range(0, len(chunks_to_embed), embed_batch_size):
        batch = chunks_to_embed[i:i + embed_batch_size]
        texts = [item['chunk'] for item in batch]

        print(f"Embedding batch {i // embed_batch_size + 1}/{(len(chunks_to_embed) + embed_batch_size - 1) // embed_batch_size}")

        # Get embeddings for this batch
        embeddings = get_embeddings(texts, cohere)

        # Create points
        for item, embedding in zip(batch, embeddings):
            point = PointStruct(
                id=item['point_id'],
                vector=embedding,
                payload={
                    **item['metadata'],
                    'content': item['chunk']
                }
            )
            points.append(point)

        # Add delay to respect rate limits (except on last batch)
        if i + embed_batch_size < len(chunks_to_embed):
            time.sleep(api_delay)

    # Upload to Qdrant in batches
    upload_batch_size = 100
    for i in range(0, len(points), upload_batch_size):
        batch = points[i:i + upload_batch_size]
        qdrant.upsert(
            collection_name=collection_name,
            points=batch
        )
        print(f"Uploaded {i + len(batch)}/{len(points)} points")

    print(f"Indexing complete! Total points: {len(points)}")


def main():
    parser = argparse.ArgumentParser(description='Index textbook content for RAG chatbot')
    parser.add_argument('--content-dir', required=True, help='Path to markdown content directory')
    parser.add_argument('--collection', default='textbook_en', help='Qdrant collection name')
    parser.add_argument('--language', default='en', choices=['en', 'ur'], help='Content language')
    parser.add_argument('--qdrant-url', default=os.getenv('QDRANT_URL', 'http://localhost:6333'))
    parser.add_argument('--qdrant-api-key', default=os.getenv('QDRANT_API_KEY', ''))
    parser.add_argument('--cohere-api-key', default=os.getenv('COHERE_API_KEY', ''))

    args = parser.parse_args()

    index_content(
        content_dir=args.content_dir,
        collection_name=args.collection,
        language=args.language,
        qdrant_url=args.qdrant_url,
        qdrant_api_key=args.qdrant_api_key,
        cohere_api_key=args.cohere_api_key
    )


if __name__ == '__main__':
    main()
