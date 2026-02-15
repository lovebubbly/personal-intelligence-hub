from datetime import UTC, datetime, timedelta

import httpx
import structlog

from intel_hub.collectors.base import BaseCollector, RawItemDTO
from intel_hub.config import get_settings
from intel_hub.services.retry import retry_external_call

logger = structlog.get_logger(__name__)


class OnchainCollector(BaseCollector):
    source_type = "onchain"

    whale_base_url = "https://api.whale-alert.io/v1/transactions"
    dune_base_url = "https://api.dune.com/api/v1/query"

    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = httpx.Client(timeout=25.0)

    @retry_external_call
    def _fetch_whale_alert(self, start_dt: datetime) -> list[dict]:
        if not self.settings.whale_alert_api_key:
            return []
        params = {
            "api_key": self.settings.whale_alert_api_key,
            "start": int(start_dt.timestamp()),
            "min_value": 500000,
        }
        response = self.client.get(self.whale_base_url, params=params)
        response.raise_for_status()
        payload = response.json()
        return payload.get("transactions", [])

    @retry_external_call
    def _fetch_dune(self) -> list[dict]:
        if not self.settings.dune_api_key:
            return []

        # Placeholder query for MVP. Query ID should be configured per deployment.
        query_id = "0"
        url = f"{self.dune_base_url}/{query_id}/results"
        headers = {"X-Dune-API-Key": self.settings.dune_api_key}
        response = self.client.get(url, headers=headers)
        response.raise_for_status()
        payload = response.json()
        return payload.get("result", {}).get("rows", [])

    def collect(self, domain_id: str, since: datetime | None = None) -> list[RawItemDTO]:
        start_dt = since or datetime.now(UTC) - timedelta(minutes=10)
        items: list[RawItemDTO] = []

        try:
            whale_events = self._fetch_whale_alert(start_dt)
            items.extend([self.normalize({"provider": "whale_alert", "event": event}, domain_id) for event in whale_events])
        except Exception as exc:
            logger.warning("onchain_whale_collect_failed", domain=domain_id, error=str(exc))

        try:
            dune_rows = self._fetch_dune()
            items.extend([self.normalize({"provider": "dune", "event": row}, domain_id) for row in dune_rows])
        except Exception as exc:
            logger.warning("onchain_dune_collect_failed", domain=domain_id, error=str(exc))

        return items

    def normalize(self, payload: dict, domain_id: str) -> RawItemDTO:
        provider = payload["provider"]
        event = payload["event"]

        if provider == "whale_alert":
            source_id = str(event.get("id") or event.get("transaction_id") or event.get("hash"))
            amount = event.get("amount", 0)
            symbol = event.get("symbol", "UNKNOWN")
            content = f"Whale transfer detected: {amount} {symbol}"
            url = event.get("transaction_id")
            if url:
                url = f"https://www.blockchain.com/explorer/transactions/btc/{url}"
        else:
            source_id = str(event.get("id") or event.get("tx_hash") or hash(str(event)))
            content = event.get("summary") or f"Dune signal: {event}"
            url = event.get("url")

        return RawItemDTO(
            domain_id=domain_id,
            source_type=self.source_type,
            source_id=source_id,
            author=provider,
            content=content,
            url=url,
            raw_metadata={"provider": provider, "event": event},
            collected_at=datetime.now(UTC),
        )
