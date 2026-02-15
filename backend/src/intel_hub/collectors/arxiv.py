from datetime import UTC, datetime, timedelta

import feedparser
import structlog

from intel_hub.collectors.base import BaseCollector, RawItemDTO

logger = structlog.get_logger(__name__)


class ArxivCollector(BaseCollector):
    source_type = "arxiv"

    def collect(self, domain_id: str, since: datetime | None = None) -> list[RawItemDTO]:
        if domain_id != "ai_ml":
            return []

        start_dt = since or datetime.now(UTC) - timedelta(days=1)
        query = "cat:cs.AI+OR+cat:cs.CL+OR+cat:cs.LG"
        url = (
            "http://export.arxiv.org/api/query"
            f"?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results=30"
        )

        try:
            feed = feedparser.parse(url)
        except Exception as exc:
            logger.warning("arxiv_collect_failed", domain=domain_id, error=str(exc))
            return []

        items: list[RawItemDTO] = []
        for entry in feed.entries:
            updated = entry.get("updated_parsed")
            entry_dt = datetime.now(UTC)
            if updated:
                entry_dt = datetime(*updated[:6], tzinfo=UTC)
            if entry_dt < start_dt:
                continue
            items.append(self.normalize({"entry": entry}, domain_id))

        return items

    def normalize(self, payload: dict, domain_id: str) -> RawItemDTO:
        entry = payload["entry"]
        source_id = entry.get("id", "").split("/")[-1]
        authors = [author.get("name") for author in entry.get("authors", [])]
        categories = [tag.get("term") for tag in entry.get("tags", [])]

        return RawItemDTO(
            domain_id=domain_id,
            source_type=self.source_type,
            source_id=source_id,
            author=", ".join([a for a in authors if a]),
            content=f"{entry.get('title', '')}\n\n{entry.get('summary', '')}".strip(),
            url=entry.get("link"),
            raw_metadata={
                "categories": categories,
                "published": entry.get("published"),
                "updated": entry.get("updated"),
            },
            collected_at=datetime.now(UTC),
        )
