import json

import structlog
from pydantic import ValidationError

from intel_hub.db.models import AnalyzedItem, RawItem
from intel_hub.db.repository import HubRepository
from intel_hub.domains.registry import get_domain_registry
from intel_hub.pipeline.llm import ClaudeClient
from intel_hub.pipeline.schemas import AnalyzerResult

logger = structlog.get_logger(__name__)


class AnalyzerPipeline:
    def __init__(self, repository: HubRepository):
        self.repo = repository
        self.registry = get_domain_registry()
        self.claude = ClaudeClient(repository)

    def _render_prompt(self, raw_item: RawItem, analyzed_item: AnalyzedItem) -> str:
        config = self.registry.get(raw_item.domain_id)
        prompt = config.analyzer_prompt
        replacements = {
            "content": raw_item.content,
            "author": raw_item.author or "unknown",
            "source_type": raw_item.source_type,
            "related_topics": ", ".join(analyzed_item.related_topics or []),
        }
        for key, value in replacements.items():
            prompt = prompt.replace(f"{{{key}}}", str(value))
        return prompt

    def run_for_analyzed_item(self, analyzed_item_id) -> dict | None:
        analyzed_item = self.repo.db.get(AnalyzedItem, analyzed_item_id)
        if analyzed_item is None:
            raise ValueError(f"analyzed_item not found: {analyzed_item_id}")

        if not analyzed_item.is_signal or (analyzed_item.importance_score or 0) < 7:
            return None

        raw_item = self.repo.get_raw_item(analyzed_item.raw_item_id)
        if raw_item is None:
            raise ValueError(f"raw_item not found for analyzed: {analyzed_item_id}")

        prompt = self._render_prompt(raw_item, analyzed_item)
        for attempt in range(2):
            try:
                payload = self.claude.generate_json(prompt)
                parsed = AnalyzerResult.model_validate(payload)
                break
            except (ValidationError, json.JSONDecodeError, KeyError) as exc:
                logger.warning(
                    "analyzer_parser_error",
                    analyzed_item_id=str(analyzed_item_id),
                    attempt=attempt + 1,
                    error=str(exc),
                )
                if attempt == 1:
                    parsed = AnalyzerResult(
                        sentiment_score=0,
                        action_signal="neutral",
                        analysis="분석 결과 파싱에 실패했습니다.",
                    )
                else:
                    prompt = prompt + "\n\nRespond with strict JSON only."

        updated_payload = {
            "raw_item_id": analyzed_item.raw_item_id,
            "domain_id": analyzed_item.domain_id,
            "is_signal": analyzed_item.is_signal,
            "noise_reason": analyzed_item.noise_reason,
            "importance_score": analyzed_item.importance_score,
            "sentiment_score": parsed.sentiment_score,
            "action_signal": parsed.action_signal,
            "context_summary": parsed.analysis,
            "related_topics": analyzed_item.related_topics,
            "category": analyzed_item.category,
            "llm_model": "claude-3-5-sonnet-latest",
        }
        updated_id = self.repo.upsert_analyzed_item(updated_payload)
        return {
            "analyzed_id": updated_id,
            "raw_item_id": analyzed_item.raw_item_id,
            "domain_id": analyzed_item.domain_id,
        }
