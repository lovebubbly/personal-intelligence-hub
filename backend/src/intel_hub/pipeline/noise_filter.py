import json

import structlog
from pydantic import ValidationError

from intel_hub.db.models import RawItem
from intel_hub.db.repository import HubRepository
from intel_hub.domains.registry import get_domain_registry
from intel_hub.pipeline.llm import GeminiClient
from intel_hub.pipeline.schemas import NoiseFilterResult

logger = structlog.get_logger(__name__)


class NoiseFilterPipeline:
    def __init__(self, repository: HubRepository):
        self.repo = repository
        self.registry = get_domain_registry()
        self.gemini = GeminiClient(repository)

    def _render_prompt(self, raw_item: RawItem, credibility_score: float) -> str:
        domain_config = self.registry.get(raw_item.domain_id)
        prompt = domain_config.noise_filter_prompt
        replacements = {
            "content": raw_item.content,
            "author": raw_item.author or "unknown",
            "source_type": raw_item.source_type,
            "credibility_score": credibility_score,
        }
        for key, value in replacements.items():
            prompt = prompt.replace(f"{{{key}}}", str(value))
        return prompt

    def _resolve_credibility(self, domain_id: str, author: str | None) -> float:
        if not author:
            return 0.50
        kols = self.repo.list_kols(domain_id)
        for kol in kols:
            if kol.twitter_username.lower() == author.lower().replace("@", ""):
                return float(kol.credibility_score)
        return 0.50

    def run_for_raw_item(self, raw_item_id) -> dict:
        raw_item = self.repo.get_raw_item(raw_item_id)
        if raw_item is None:
            raise ValueError(f"raw_item not found: {raw_item_id}")

        credibility_score = self._resolve_credibility(raw_item.domain_id, raw_item.author)
        prompt = self._render_prompt(raw_item, credibility_score)

        for attempt in range(2):
            try:
                payload = self.gemini.generate_json(prompt)
                parsed = NoiseFilterResult.model_validate(payload)
                break
            except (ValidationError, json.JSONDecodeError, KeyError) as exc:
                logger.warning(
                    "noise_filter_parser_error",
                    raw_item_id=str(raw_item_id),
                    attempt=attempt + 1,
                    error=str(exc),
                )
                if attempt == 1:
                    parsed = NoiseFilterResult(
                        is_signal=False,
                        noise_reason="parser_error",
                        importance_score=1,
                        related_topics=[],
                        category="other",
                        context_summary="파싱 오류로 신호 판별에 실패했습니다.",
                    )
                else:
                    prompt = (
                        prompt
                        + "\n\nReturn valid JSON object only. No markdown. All required keys must exist."
                    )

        analyzed_payload = {
            "raw_item_id": raw_item.id,
            "domain_id": raw_item.domain_id,
            "is_signal": parsed.is_signal,
            "noise_reason": parsed.noise_reason,
            "importance_score": parsed.importance_score,
            "sentiment_score": 0,
            "action_signal": "neutral",
            "context_summary": parsed.context_summary,
            "related_topics": parsed.related_topics,
            "category": parsed.category,
            "llm_model": "gemini-2.0-flash",
        }
        analyzed_id = self.repo.upsert_analyzed_item(analyzed_payload)
        return {"analyzed_id": analyzed_id, "raw_item_id": raw_item.id, "domain_id": raw_item.domain_id}
