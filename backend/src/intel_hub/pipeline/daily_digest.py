from collections import defaultdict
from datetime import UTC, date, datetime, time, timedelta

from intel_hub.db.repository import HubRepository
from intel_hub.pipeline.llm import ClaudeClient
from intel_hub.pipeline.schemas import DigestResult


class DailyDigestPipeline:
    def __init__(self, repository: HubRepository):
        self.repo = repository
        self.claude = ClaudeClient(repository)

    def _time_range_for_day(self, target_date: date) -> tuple[datetime, datetime]:
        start = datetime.combine(target_date, time.min, tzinfo=UTC)
        end = datetime.combine(target_date, time.max, tzinfo=UTC)
        return start, end

    def run(self, domain_id: str, target_date: date | None = None) -> list[dict]:
        if target_date is None:
            target_date = date.today() - timedelta(days=1)

        start_dt, end_dt = self._time_range_for_day(target_date)
        items = self.repo.analyzed_items_for_digest(domain_id, start_dt, end_dt)

        grouped: dict[str, list[dict]] = defaultdict(list)
        for item in items:
            for topic in item.get("related_topics") or ["GENERAL"]:
                grouped[topic].append(item)

        results = []
        for topic, topic_items in grouped.items():
            prompt = self._build_prompt(domain_id, topic, topic_items)
            payload = self.claude.generate_json(prompt)
            digest = DigestResult.model_validate(payload)

            sentiment_avg = int(
                sum((x.get("sentiment_score") or 0) for x in topic_items) / max(len(topic_items), 1)
            )
            top_events = [
                {
                    "content": x.get("content"),
                    "url": x.get("url"),
                    "action_signal": x.get("action_signal"),
                }
                for x in sorted(topic_items, key=lambda x: x.get("importance_score", 0), reverse=True)[:5]
            ]
            payload = {
                "domain_id": domain_id,
                "topic": topic,
                "digest_date": target_date,
                "summary": digest.summary,
                "detailed_analysis": digest.detailed_analysis,
                "sentiment_avg": sentiment_avg,
                "signal_count": len(topic_items),
                "top_events": top_events,
            }
            digest_id = self.repo.upsert_digest(payload)
            results.append({"id": str(digest_id), **payload})

        return results

    def _build_prompt(self, domain_id: str, topic: str, items: list[dict]) -> str:
        headlines = "\n".join(
            [
                f"- importance={item.get('importance_score')} signal={item.get('action_signal')} content={item.get('content')}"
                for item in items[:20]
            ]
        )
        return (
            f"도메인: {domain_id}\n"
            f"토픽: {topic}\n"
            "지난 24시간 주요 이벤트를 한국어로 요약하라."
            "JSON만 출력: {\"summary\":\"1문장\",\"detailed_analysis\":\"3문장\"}.\n"
            f"입력 이벤트:\n{headlines}"
        )
