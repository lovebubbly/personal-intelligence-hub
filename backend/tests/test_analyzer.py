from dataclasses import dataclass
from uuid import UUID, uuid4

from intel_hub.pipeline.analyzer import AnalyzerPipeline


@dataclass
class RawItemStub:
    id: UUID
    domain_id: str
    source_type: str
    author: str | None
    content: str


@dataclass
class AnalyzedItemStub:
    id: UUID
    raw_item_id: UUID
    domain_id: str
    is_signal: bool
    importance_score: int
    noise_reason: str | None
    related_topics: list[str]
    category: str


class DBStub:
    def __init__(self, analyzed_item):
        self._analyzed_item = analyzed_item

    def get(self, model, analyzed_item_id):
        return self._analyzed_item


class RepoStub:
    def __init__(self):
        raw_id = uuid4()
        self.raw_item = RawItemStub(
            id=raw_id,
            domain_id="crypto",
            source_type="twitter",
            author="author",
            content="content",
        )
        self.analyzed_item = AnalyzedItemStub(
            id=uuid4(),
            raw_item_id=raw_id,
            domain_id="crypto",
            is_signal=True,
            importance_score=8,
            noise_reason=None,
            related_topics=["BTC"],
            category="macro",
        )
        self.db = DBStub(self.analyzed_item)
        self.saved_payload = None

    def get_raw_item(self, raw_item_id):
        return self.raw_item

    def upsert_analyzed_item(self, payload):
        self.saved_payload = payload
        return uuid4()


class ClaudeStub:
    def generate_json(self, prompt):
        return {"sentiment_score": 17, "action_signal": "watch", "analysis": "테스트 분석"}


def test_analyzer_updates_signal_payload():
    repo = RepoStub()
    pipeline = AnalyzerPipeline(repo)
    pipeline.claude = ClaudeStub()

    pipeline.run_for_analyzed_item(repo.analyzed_item.id)

    assert repo.saved_payload is not None
    assert repo.saved_payload["action_signal"] == "watch"
    assert repo.saved_payload["sentiment_score"] == 17
