"""
Embedding Generation Utilities (Lightweight Version)
Uses OpenAI API or simple numerical embeddings
"""

import logging
import os
import hashlib
from typing import List
import numpy as np

logger = logging.getLogger(__name__)

# Simple embedding dimension (compatible with SurrealDB)
EMBEDDING_DIM = 384

async def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding vector for text
    Uses OpenAI if API key available, otherwise creates simple numerical embedding
    """
    try:
        # Try OpenAI first if API key is available
        if os.getenv("USE_OPENAI", "false").lower() == "true" and os.getenv("OPENAI_API_KEY"):
            return await generate_openai_embedding(text)
        else:
            # Fall back to simple numerical embedding
            return generate_simple_embedding(text)
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        # Return a valid random embedding as fallback
        return generate_simple_embedding(text)

async def generate_openai_embedding(text: str) -> List[float]:
    """Generate embedding using OpenAI API"""
    try:
        from openai import AsyncOpenAI
        
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = await client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
            dimensions=EMBEDDING_DIM
        )
        
        embedding = response.data[0].embedding
        logger.info(f"Generated OpenAI embedding with {len(embedding)} dimensions")
        return embedding
        
    except Exception as e:
        logger.warning(f"OpenAI embedding failed: {e}, falling back to simple embedding")
        return generate_simple_embedding(text)

def generate_simple_embedding(text: str) -> List[float]:
    """
    Generate a simple but consistent numerical embedding from text
    This is a deterministic approach that works without external models
    """
    # Create a consistent hash-based seed from the text
    text_hash = hashlib.sha256(text.encode()).digest()
    seed = int.from_bytes(text_hash[:4], byteorder='big')
    
    # Use numpy for consistent random generation based on text
    rng = np.random.RandomState(seed)
    
    # Generate base embedding
    embedding = rng.randn(EMBEDDING_DIM).astype(float)
    
    # Normalize to unit vector (important for cosine similarity)
    norm = np.linalg.norm(embedding)
    if norm > 0:
        embedding = embedding / norm
    
    # Add some text-specific features to make similar texts more similar
    text_lower = text.lower()
    common_words = ['docker', 'compose', 'container', 'agent', 'database', 'surreal', 
                    'memory', 'search', 'query', 'ai', 'system', 'service']
    
    for i, word in enumerate(common_words):
        if word in text_lower:
            # Boost specific dimensions for this word
            dim_index = (i * 30) % EMBEDDING_DIM
            embedding[dim_index:dim_index + 5] += 0.1
    
    # Re-normalize after adding features
    norm = np.linalg.norm(embedding)
    if norm > 0:
        embedding = embedding / norm
    
    return embedding.tolist()

async def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """Generate embeddings for multiple texts"""
    try:
        if os.getenv("USE_OPENAI", "false").lower() == "true" and os.getenv("OPENAI_API_KEY"):
            from openai import AsyncOpenAI
            
            client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = await client.embeddings.create(
                model="text-embedding-3-small",
                input=texts,
                dimensions=EMBEDDING_DIM
            )
            
            embeddings = [item.embedding for item in response.data]
            logger.info(f"Generated {len(embeddings)} OpenAI embeddings")
            return embeddings
        else:
            return [generate_simple_embedding(text) for text in texts]
            
    except Exception as e:
        logger.error(f"Error generating batch embeddings: {e}")
        return [generate_simple_embedding(text) for text in texts]
