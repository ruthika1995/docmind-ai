import json
import logging
from typing import Dict, Any
from app.ai.openrouter_client import openrouter_client
from app.ai.prompts import SUMMARIZATION_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class DocumentSummarizer:
    """
    Generates multi-tier syntheses (executive, bullet takeaways, TL;DR, action items) via OpenRouter.
    """
    def __init__(self):
        self.client = openrouter_client

    async def summarize(self, text: str, title: str = "") -> Dict[str, Any]:
        sample_text = text[:9000] if len(text) > 9000 else text
        user_prompt = f"Document Title: {title}\n\nDocument Text:\n\"\"\"\n{sample_text}\n\"\"\"\n\nProvide the structured multi-format summary."

        response = await self.client.generate_completion(
            prompt=user_prompt,
            system_prompt=SUMMARIZATION_SYSTEM_PROMPT,
            temperature=0.2,
            response_format={"type": "json_object"},
            task_type="summarize"
        )

        content = response.get("content", "{}")
        try:
            data = json.loads(content)
            return {
                "executive": data.get("executive", "Summary generated."),
                "bullets": data.get("bullets", []),
                "tldr": data.get("tldr", ""),
                "action_items": data.get("action_items", []),
                "model_used": response.get("model", "openrouter")
            }
        except Exception as e:
            logger.warning(f"Summarizer parsing error: {e}")
            return {
                "executive": content,
                "bullets": [],
                "tldr": "",
                "action_items": [],
                "model_used": response.get("model", "openrouter")
            }

summarizer_service = DocumentSummarizer()
