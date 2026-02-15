import hashlib
from datetime import UTC, datetime

import feedparser
import structlog

from intel_hub.collectors.base import BaseCollector, RawItemDTO
from intel_hub.domains.registry import get_domain_registry

logger = structlog.get_logger(__name__)


class RSSCollector(BaseCollector):
    source_type = "news"

    def __init__(self) -> None:
        self.registry = get_domain_registry()

    def collect(self, domain_id: str, since: datetime | None = None) -> list[RawItemDTO]:
        config = self.registry.get(domain_id)
        items: list[RawItemDTO] = []

        for source_url in config.rss_sources:
            try:
                feed = feedparser.parse(source_url)
            except Exception as exc:
                logger.warning("rss_collect_failed", domain=domain_id, source=source_url, error=str(exc))
                continue

            for entry in feed.entries[:30]:
                items.append(
                    self.normalize(
                        {
                            "entry": entry,
                            "source_url": source_url,
                            "feed_title": feed.feed.get("title", "Unknown Feed"),
                        },
                        domain_id,
                    )
                )
        return items

    def normalize(self, payload: dict, domain_id: str) -> RawItemDTO:
        entry = payload["entry"]
        source_url = payload["source_url"]
        canonical = entry.get("link", "")
        source_id = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:32]

        published = entry.get("published") or entry.get("updated")
        summary = entry.get("summary", "")
        title = entry.get("title", "")
        content = f"{title}\n\n{summary}".strip()

        return RawItemDTO(
            domain_id=domain_id,
            source_type=self.source_type,
            source_id=source_id,
            author=entry.get("author"),
            content=content,
            url=canonical,
            raw_metadata={
                "published_at": published,
                "source_name": payload["feed_title"],
                "source_url": source_url,
            },
            collected_at=datetime.now(UTC),
        )
