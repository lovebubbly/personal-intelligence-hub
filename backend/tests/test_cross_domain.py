from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from intel_hub.pipeline.cross_domain import CrossDomainLinkPipeline


class RepoStub:
    def __init__(self):
        self.created: list[tuple] = []
        self._existing = set()
        self.source_id = uuid4()
        self.target_id = uuid4()

    def recent_signal_items(self, since: datetime):
        return [
            {
                "analyzed_item_id": self.source_id,
                "domain_id": "crypto",
                "related_topics": ["NVIDIA", "GPU"],
                "importance_score": 8,
                "action_signal": "watch",
                "content": "NVIDIA chip regulation update",
                "context_summary": "AI 칩 규제 강화",
            },
            {
                "analyzed_item_id": self.target_id,
                "domain_id": "ai_ml",
                "related_topics": ["NVIDIA", "Agent"],
                "importance_score": 8,
                "action_signal": "learn",
                "content": "GPU 공급 이슈가 모델 학습 비용에 영향",
                "context_summary": "인프라 비용 상승",
            },
        ]

    def has_cross_domain_link(self, source_item_id, target_item_id):
        key = tuple(sorted((str(source_item_id), str(target_item_id))))
        return key in self._existing

    def create_cross_domain_link(self, source_item_id, target_item_id, link_type, explanation, confidence):
        self.created.append((source_item_id, target_item_id, link_type, explanation, confidence))
        key = tuple(sorted((str(source_item_id), str(target_item_id))))
        self._existing.add(key)
        return uuid4()


def test_cross_domain_pipeline_creates_link_on_topic_overlap():
    repo = RepoStub()
    pipeline = CrossDomainLinkPipeline(repo)

    count = pipeline.run(recent_minutes=30)

    assert count == 1
    assert len(repo.created) == 1
    _, _, link_type, _, confidence = repo.created[0]
    assert link_type in {"related", "causal"}
    assert isinstance(confidence, Decimal)


def test_cross_domain_pipeline_is_idempotent_for_existing_pair():
    repo = RepoStub()
    pipeline = CrossDomainLinkPipeline(repo)

    first = pipeline.run(recent_minutes=30)
    second = pipeline.run(recent_minutes=30)

    assert first == 1
    assert second == 0
