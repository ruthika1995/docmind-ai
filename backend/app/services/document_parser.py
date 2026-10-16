import io
import re
import logging
from typing import List, Dict, Any, Tuple
from pypdf import PdfReader
from docx import Document as DocxDocument
from app.ai.embeddings import embedding_engine

logger = logging.getLogger(__name__)

class DocumentParser:
    """
    Parses and chunks PDF, DOCX, TXT, and Markdown files into grounded semantic passages.
    """
    @staticmethod
    def parse_pdf(file_bytes: bytes) -> Tuple[str, List[Dict[str, Any]]]:
        """Extracts text and page-indexed chunks from PDF bytes."""
        reader = PdfReader(io.BytesIO(file_bytes))
        full_text_parts = []
        pages_content = []

        for idx, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            page_num = idx + 1
            full_text_parts.append(page_text)
            pages_content.append({"page": page_num, "text": page_text})

        full_text = "\n\n".join(full_text_parts)
        return full_text, pages_content

    @staticmethod
    def parse_docx(file_bytes: bytes) -> Tuple[str, List[Dict[str, Any]]]:
        """Extracts text from DOCX bytes."""
        doc = DocxDocument(io.BytesIO(file_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        full_text = "\n\n".join(paragraphs)
        pages_content = [{"page": 1, "text": full_text}]
        return full_text, pages_content

    @staticmethod
    def parse_text(file_bytes: bytes) -> Tuple[str, List[Dict[str, Any]]]:
        """Extracts plain text/markdown bytes."""
        try:
            full_text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            full_text = file_bytes.decode("latin-1", errors="ignore")
        pages_content = [{"page": 1, "text": full_text}]
        return full_text, pages_content

    @classmethod
    def extract_text_and_chunks(
        cls,
        file_bytes: bytes,
        file_type: str,
        chunk_size: int = 600,
        chunk_overlap: int = 100
    ) -> Tuple[str, List[Dict[str, Any]]]:
        ft = file_type.lower().strip().replace(".", "")
        if ft == "pdf":
            raw_text, pages_content = cls.parse_pdf(file_bytes)
        elif ft in ["docx", "doc"]:
            raw_text, pages_content = cls.parse_docx(file_bytes)
        else:
            raw_text, pages_content = cls.parse_text(file_bytes)

        chunks: List[Dict[str, Any]] = []
        chunk_index = 0

        for page_item in pages_content:
            page_num = page_item["page"]
            page_text = page_item["text"].strip()
            if not page_text:
                continue

            # Split into paragraphs or sentences
            paras = re.split(r'\n{2,}', page_text)
            current_chunk = ""

            for p in paras:
                p_clean = p.strip()
                if not p_clean:
                    continue

                if len(current_chunk) + len(p_clean) < chunk_size:
                    current_chunk += ("\n" + p_clean if current_chunk else p_clean)
                else:
                    if current_chunk:
                        emb = embedding_engine.embed_text(current_chunk)
                        chunks.append({
                            "chunk_index": chunk_index,
                            "content": current_chunk,
                            "page_number": page_num,
                            "token_count": len(current_chunk.split()),
                            "embedding": emb
                        })
                        chunk_index += 1
                    current_chunk = p_clean

            if current_chunk:
                emb = embedding_engine.embed_text(current_chunk)
                chunks.append({
                    "chunk_index": chunk_index,
                    "content": current_chunk,
                    "page_number": page_num,
                    "token_count": len(current_chunk.split()),
                    "embedding": emb
                })
                chunk_index += 1

        # If document had no paragraphs, ensure at least one chunk exists
        if not chunks and raw_text.strip():
            emb = embedding_engine.embed_text(raw_text)
            chunks.append({
                "chunk_index": 0,
                "content": raw_text[:chunk_size],
                "page_number": 1,
                "token_count": len(raw_text.split()),
                "embedding": emb
            })

        return raw_text, chunks

document_parser = DocumentParser()
