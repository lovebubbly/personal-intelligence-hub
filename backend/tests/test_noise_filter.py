from dataclasses import dataclass
from uuid import UUID, uuid4

from intel_hub.pipeline.noise_filter import NoiseFilterPipeline


@dataclass
class RawItemStub:
    id: UUID
    domain_id: str
    source_type: str
    author: str | None
    content: str


class RepoStub:
    def __init__(self):
        self.raw_item = RawItemStub(
            id=uuid4(),
            domain_id="crypto",
            source_type="twitter",
            author="someone",
            content="Random noisy content",
        )
        self.saved_payload = None

    def get_raw_item(self, raw_item_id):
        return self.raw_item

    def list_kols(self, domain_id):
        return []

    def upsert_analyzed_item(self, payload):
        self.saved_payload = payload
        return uuid4()


class GeminiStub:
    def __init__(self):
        self.calls = 0

    def generate_json(self, prompt):
        self.calls += 1
        return {"broken": True}


def test_noise_filter_falls_back_to_parser_error():
    repo = RepoStub()
    pipeline = NoiseFilterPipeline(repo)
    pipeline.gemini = GeminiStub()

    pipeline.run_for_raw_item(repo.raw_item.id)

    assert repo.saved_payload is not None
    assert repo.saved_payload["is_signal"] is False
    assert repo.saved_payload["noise_reason"] == "parser_error"
