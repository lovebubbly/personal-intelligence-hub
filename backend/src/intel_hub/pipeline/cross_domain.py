from datetime import UTC, datetime, timedelta
from decimal import Decimal

import structlog

from intel_hub.db.repository import HubRepository

logger = structlog.get_logger(__name__)


BRIDGE_KEYWORDS = {
    "nvidia",
    "gpu",
    "chip",
    "regulation",
    "sec",
    "etf",
    "stablecoin",
    "agent",
    "openai",
    "anthropic",
    "token",
}


class CrossDomainLinkPipeline:
    def __init__(self, repository: HubRepository):
        self.repo = repository

    def run(self, recent_minutes: int = 30) -> int:
        since = datetime.now(UTC) - timedelta(minutes=recent_minutes)
        items = self.repo.recent_signal_items(since)

        links_created = 0
        for idx, source in enumerate(items):
            for target in items[idx + 1 :]:
                if source["domain_id"] == target["domain_id"]:
                    continue

                link = self._infer_link(source, target)
                if link is None:
                    continue

                source_id = source["analyzed_item_id"]
                target_id = target["analyzed_item_id"]
                if self.repo.has_cross_domain_link(source_id, target_id):
                    continue

                self.repo.create_cross_domain_link(
                    source_item_id=source_id,
                    target_item_id=target_id,
                    link_type=link["link_type"],
                    explanation=link["explanation"],
                    confidence=Decimal(str(link["confidence"])),
                )
                links_created += 1

        logger.info("cross_domain_links_created", count=links_created)
        return links_created

    def _infer_link(self, source: dict, target: dict) -> dict | None:
        src_topics = set((source.get("related_topics") or []))
        tgt_topics = set((target.get("related_topics") or []))
        overlap = src_topics.intersection(tgt_topics)
        if overlap:
            topic_text = ", ".join(sorted(overlap))
            return {
                "link_type": "related",
                "explanation": f"공통 토픽({topic_text}) 기반으로 도메인 간 연관성이 높습니다.",
                "confidence": 0.82,
            }

        src_text = f"{source.get('content', '')} {source.get('context_summary', '')}".lower()
        tgt_text = f"{target.get('content', '')} {target.get('context_summary', '')}".lower()

        matched_keywords = [keyword for keyword in BRIDGE_KEYWORDS if keyword in src_text and keyword in tgt_text]
        if matched_keywords:
            keyword_text = ", ".join(sorted(matched_keywords))
            return {
                "link_type": "causal",
                "explanation": f"공통 키워드({keyword_text})가 관측되어 도메인 간 인과 가능성이 있습니다.",
                "confidence": 0.74,
            }

        return None
