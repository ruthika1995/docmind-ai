import json
import logging
from typing import Dict, Any
from app.ai.openrouter_client import openrouter_client
from app.ai.prompts import CLASSIFIER_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class DocumentClassifier:
    """
    Classifies raw document text into taxonomy categories using OpenRouter gateway.
    """
    def __init__(self):
        self.client = openrouter_client

    async def classify(self, text: str, filename: str = "") -> Dict[str, Any]:
        sample_text = text[:3500] if len(text) > 3500 else text
        user_prompt = f"Filename: {filename}\n\nDocument Excerpt:\n\"\"\"\n{sample_text}\n\"\"\"\n\nClassify this document."
        
        response = await self.client.generate_completion(
            prompt=user_prompt,
            system_prompt=CLASSIFIER_SYSTEM_PROMPT,
            temperature=0.1,
            response_format={"type": "json_object"},
            task_type="classify"
        )
        
        content = response.get("content", "{}")
        try:
            data = json.loads(content)
            category = data.get("category", "general")
            confidence = float(data.get("confidence", 0.85))
            reason = data.get("reason", "Automated classification.")
            metadata = data.get("metadata", {})
            return {
                "category": category,
                "confidence": confidence,
                "reason": reason,
                "metadata": metadata,
                "model_used": response.get("model", "openrouter")
            }
        except Exception as e:
            logger.warning(f"Failed to parse classification JSON: {e}. Raw content: {content}")
            return {
                "category": "general",
                "confidence": 0.70,
                "reason": "General document structure recognized.",
                "metadata": {},
                "model_used": response.get("model", "openrouter")
            }

classifier_service = DocumentClassifier()
