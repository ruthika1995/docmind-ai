import json
import logging
from typing import Dict, Any
from app.ai.openrouter_client import openrouter_client
from app.ai.prompts import COMPARATOR_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

class DocumentComparator:
    """
    Compares two contracts or document versions, extracting clause divergences and risk profiles.
    """
    def __init__(self):
        self.client = openrouter_client

    async def compare(
        self,
        doc_a_name: str,
        doc_a_text: str,
        doc_b_name: str,
        doc_b_text: str
    ) -> Dict[str, Any]:
        text_a_sample = doc_a_text[:5000] if len(doc_a_text) > 5000 else doc_a_text
        text_b_sample = doc_b_text[:5000] if len(doc_b_text) > 5000 else doc_b_text

        user_prompt = f"""=== DOCUMENT A: {doc_a_name} ===
\"\"\"
{text_a_sample}
\"\"\"

=== DOCUMENT B: {doc_b_name} ===
\"\"\"
{text_b_sample}
\"\"\"

Perform complete clause-by-clause comparison and risk audit now."""

        response = await self.client.generate_completion(
            prompt=user_prompt,
            system_prompt=COMPARATOR_SYSTEM_PROMPT,
            temperature=0.1,
            max_tokens=3500,
            response_format={"type": "json_object"},
            task_type="compare"
        )

        content = response.get("content", "{}")
        try:
            data = json.loads(content)
            return {
                "diff_summary": data.get("diff_summary", "Comparative audit completed."),
                "clauses_comparison": data.get("clauses_comparison", []),
                "risk_assessment": data.get("risk_assessment", {
                    "overall_risk": "Low",
                    "risk_factors": [],
                    "recommendations": []
                }),
                "model_used": response.get("model", "openrouter")
            }
        except Exception as e:
            logger.error(f"Failed to parse comparator JSON: {e}")
            return {
                "diff_summary": "Comparative differences detected between document versions.",
                "clauses_comparison": [],
                "risk_assessment": {"overall_risk": "Unknown", "risk_factors": [str(e)], "recommendations": []},
                "model_used": response.get("model", "openrouter")
            }

comparator_service = DocumentComparator()
