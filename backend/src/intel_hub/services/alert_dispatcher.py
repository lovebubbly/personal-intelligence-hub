import asyncio

from intel_hub.config import get_settings
from intel_hub.db.models import TelegramSubscriber
from intel_hub.telegram.bot import TelegramNotifier


class AlertDispatcher:
    def __init__(self):
        self.settings = get_settings()
        self.notifier = TelegramNotifier(self.settings.telegram_bot_token)

    def should_send(self, item: dict, subscriber: TelegramSubscriber) -> bool:
        importance = item.get("importance_score") or 0
        signal = item.get("action_signal")

        if subscriber.alert_level == "critical":
            return signal == "risk" and importance >= self.settings.risk_alert_threshold

        if subscriber.alert_level == "high":
            return importance >= self.settings.importance_alert_threshold or (
                signal == "risk" and importance >= self.settings.risk_alert_threshold
            )

        return True

    def matches_filters(self, item: dict, subscriber: TelegramSubscriber) -> bool:
        domain_filter = subscriber.domain_filter or []
        if domain_filter and item.get("domain_id") not in domain_filter:
            return False

        topic_filter = subscriber.topic_filter or []
        item_topics = item.get("related_topics") or []
        if topic_filter and not any(topic in topic_filter for topic in item_topics):
            return False

        return True

    def dispatch(self, item: dict, subscribers: list[TelegramSubscriber]) -> None:
        message = self._format_message(item)
        for subscriber in subscribers:
            if not self.should_send(item, subscriber):
                continue
            if not self.matches_filters(item, subscriber):
                continue
            asyncio.run(self.notifier.send_message(subscriber.chat_id, message))

    @staticmethod
    def _format_message(item: dict) -> str:
        domain = "🪙" if item.get("domain_id") == "crypto" else "🤖"
        signal = item.get("action_signal", "neutral").upper()
        summary = item.get("context_summary") or "요약 없음"
        author = item.get("author") or "unknown"
        content = item.get("content") or ""
        url = item.get("url") or ""
        topics = ", ".join(item.get("related_topics") or [])

        return (
            f"{domain} [{signal}] {topics}\n"
            f"📡 {author}: {content[:220]}\n"
            f"💡 {summary}\n"
            f"🔗 {url}"
        )
