from datetime import UTC, datetime, timedelta

import httpx
import structlog

from intel_hub.collectors.base import BaseCollector, RawItemDTO
from intel_hub.config import get_settings
from intel_hub.domains.registry import get_domain_registry
from intel_hub.services.retry import retry_external_call

logger = structlog.get_logger(__name__)


class TwitterCollector(BaseCollector):
    source_type = "twitter"
    base_url = "https://api.twitter.com/2/tweets/search/recent"

    def __init__(self) -> None:
        self.settings = get_settings()
        self.registry = get_domain_registry()
        self.client = httpx.Client(timeout=20.0)

    @retry_external_call
    def _fetch_user_tweets(self, username: str, start_time: datetime) -> list[dict]:
        params = {
            "query": f"from:{username} -is:retweet",
            "tweet.fields": "created_at,public_metrics,author_id,entities",
            "max_results": 25,
            "start_time": start_time.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        }
        headers = {"Authorization": f"Bearer {self.settings.twitter_bearer_token}"}
        response = self.client.get(self.base_url, params=params, headers=headers)
        response.raise_for_status()
        payload = response.json()
        return payload.get("data", [])

    def collect(self, domain_id: str, since: datetime | None = None) -> list[RawItemDTO]:
        config = self.registry.get(domain_id)
        now = datetime.now(UTC)
        start_time = since or now - timedelta(minutes=10)

        items: list[RawItemDTO] = []
        for kol in config.kol_list:
            username = kol["username"]
            try:
                tweets = self._fetch_user_tweets(username, start_time)
            except Exception as exc:
                logger.warning(
                    "twitter_collect_failed",
                    domain=domain_id,
                    username=username,
                    error=str(exc),
                )
                continue
            for tweet in tweets:
                items.append(self.normalize(tweet, domain_id))
        return items

    def normalize(self, payload: dict, domain_id: str) -> RawItemDTO:
        metrics = payload.get("public_metrics", {})
        entities = payload.get("entities", {})
        media_urls = {"urls": [x.get("expanded_url") for x in entities.get("urls", [])]}

        return RawItemDTO(
            domain_id=domain_id,
            source_type=self.source_type,
            source_id=payload["id"],
            author=payload.get("author_id"),
            content=payload.get("text", ""),
            url=f"https://x.com/i/web/status/{payload['id']}",
            media_urls=media_urls,
            raw_metadata={
                "like_count": metrics.get("like_count", 0),
                "retweet_count": metrics.get("retweet_count", 0),
                "quote_count": metrics.get("quote_count", 0),
                "reply_count": metrics.get("reply_count", 0),
            },
            collected_at=datetime.now(UTC),
        )
