import json
import logging
from typing import Dict, Any, Optional
from app.ai.openrouter_client import openrouter_client
from app.ai.prompts import (
    INVOICE_EXTRACTION_PROMPT,
    CONTRACT_EXTRACTION_PROMPT,
    RESUME_EXTRACTION_PROMPT,
    GENERIC_EXTRACTION_PROMPT
)

logger = logging.getLogger(__name__)

class DocumentExtractor:
    """
    Extracts structured schema-compliant JSON entities from documents via OpenRouter.
    """
    def __init__(self):
        self.client = openrouter_client

    async def extract(
        self,
        text: str,
        document_type: str = "general",
        custom_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        doc_type = document_type.lower().strip()
        
        if custom_prompt:
            sys_prompt = f"You are DocMind AI's Custom Schema Extractor. Extract data matching this instruction: {custom_prompt}. Return ONLY valid JSON."
        elif doc_type == "invoice":
            sys_prompt = INVOICE_EXTRACTION_PROMPT
        elif doc_type == "contract":
            sys_prompt = CONTRACT_EXTRACTION_PROMPT
        elif doc_type == "resume":
            sys_prompt = RESUME_EXTRACTION_PROMPT
        else:
            sys_prompt = GENERIC_EXTRACTION_PROMPT

        sample_text = text[:8000] if len(text) > 8000 else text
        user_prompt = f"Target Document Text:\n\"\"\"\n{sample_text}\n\"\"\"\n\nPerform full structured extraction now."

        response = await self.client.generate_completion(
            prompt=user_prompt,
            system_prompt=sys_prompt,
            temperature=0.1,
            max_tokens=3000,
            response_format={"type": "json_object"}
        )

        content = response.get("content", "{}")
        try:
            extracted_json = json.loads(content)
            return {
                "schema_type": doc_type,
                "data": extracted_json,
                "model_used": response.get("model", "openrouter"),
                "is_mock": response.get("is_mock", False)
            }
        except Exception as e:
            logger.error(f"Failed to parse extraction JSON: {e}")
            return {
                "schema_type": doc_type,
                "data": {"raw_output": content},
                "model_used": response.get("model", "openrouter"),
                "is_mock": response.get("is_mock", False)
            }

extractor_service = DocumentExtractor()
