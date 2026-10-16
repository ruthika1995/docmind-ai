import re
import logging
from typing import List, Dict, Any, Optional, AsyncGenerator
from app.ai.openrouter_client import openrouter_client
from app.ai.embeddings import embedding_engine
from app.ai.prompts import RAG_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class RAGService:
    """
    Retrieval-Augmented Generation Service.
    Retrieves semantically grounded chunks using the decoupled embedding engine
    and generates citation-backed answers via OpenRouter.
    """
    def __init__(self):
        self.client = openrouter_client
        self.embeddings = embedding_engine

    def retrieve_relevant_chunks(
        self,
        query: str,
        chunks: List[Any],
        top_k: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Ranks document chunks by cosine similarity to the query embedding.
        """
        if not chunks:
            return []

        query_vec = self.embeddings.embed_text(query)
        scored_chunks = []

        for chunk in chunks:
            chunk_vec = chunk.embedding
            # If chunk has no cached embedding, compute it
            if not chunk_vec or not isinstance(chunk_vec, list):
                chunk_vec = self.embeddings.embed_text(chunk.content)
            
            sim = self.embeddings.cosine_similarity(query_vec, chunk_vec)
            scored_chunks.append({
                "chunk_id": chunk.id,
                "chunk_index": chunk.chunk_index,
                "page_number": chunk.page_number,
                "content": chunk.content,
                "relevance_score": round(sim, 4)
            })

        # Sort descending by relevance score
        scored_chunks.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored_chunks[:top_k]

    async def answer_question(
        self,
        query: str,
        chunks: List[Any],
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generates a grounded citation-backed answer for the question.
        """
        top_chunks = self.retrieve_relevant_chunks(query, chunks, top_k=4)
        
        context_blocks = []
        for i, c in enumerate(top_chunks):
            context_blocks.append(
                f"[Chunk {i+1} | Page {c['page_number']}]:\n{c['content']}"
            )
        
        context_str = "\n\n".join(context_blocks)
        
        user_prompt = f"""Verified Document Context Excerpts:
\"\"\"
{context_str}
\"\"\"

User Question: {query}

Provide a direct, grounded response citing relevant [Chunk X] references."""

        response = await self.client.generate_completion(
            prompt=user_prompt,
            system_prompt=RAG_SYSTEM_PROMPT,
            model=model,
            temperature=0.2
        )

        content = response.get("content", "")
        
        # Build structured citations
        citations = []
        for i, c in enumerate(top_chunks):
            marker = f"[Chunk {i+1}]"
            # Include citation if cited in response or has high relevance
            if marker in content or c["relevance_score"] > 0.45 or i == 0:
                citations.append({
                    "chunk_id": c["chunk_id"],
                    "chunk_index": c["chunk_index"],
                    "page_number": c["page_number"],
                    "snippet": c["content"][:200] + ("..." if len(c["content"]) > 200 else ""),
                    "relevance_score": c["relevance_score"]
                })

        return {
            "content": content,
            "citations": citations,
            "model_used": response.get("model", "openrouter"),
            "is_mock": response.get("is_mock", False)
        }

    async def stream_answer_question(
        self,
        query: str,
        chunks: List[Any],
        model: Optional[str] = None
    ) -> AsyncGenerator[str, None]:
        """
        Streams grounded RAG tokens.
        """
        top_chunks = self.retrieve_relevant_chunks(query, chunks, top_k=4)
        context_blocks = [
            f"[Chunk {i+1} | Page {c['page_number']}]:\n{c['content']}"
            for i, c in enumerate(top_chunks)
        ]
        context_str = "\n\n".join(context_blocks)
        
        user_prompt = f"""Verified Document Context Excerpts:
\"\"\"
{context_str}
\"\"\"

User Question: {query}

Provide a direct, grounded response citing relevant [Chunk X] references."""

        async for token in self.client.generate_stream(
            prompt=user_prompt,
            system_prompt=RAG_SYSTEM_PROMPT,
            model=model,
            temperature=0.2
        ):
            yield token

rag_service = RAGService()
