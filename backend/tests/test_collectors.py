from intel_hub.collectors.arxiv import ArxivCollector
from intel_hub.collectors.github import GitHubCollector
from intel_hub.collectors.onchain import OnchainCollector
from intel_hub.collectors.rss import RSSCollector
from intel_hub.collectors.twitter import TwitterCollector


def test_twitter_normalize_maps_metrics():
    collector = TwitterCollector()
    dto = collector.normalize(
        {
            "id": "1",
            "text": "hello",
            "author_id": "alice",
            "public_metrics": {"like_count": 4, "retweet_count": 2, "quote_count": 1, "reply_count": 0},
            "entities": {"urls": [{"expanded_url": "https://example.com"}]},
        },
        "crypto",
    )

    assert dto.source_id == "1"
    assert dto.raw_metadata["like_count"] == 4


def test_rss_normalize_hashes_source_id():
    collector = RSSCollector()
    dto = collector.normalize(
        {
            "entry": {"link": "https://news.example/a", "title": "T", "summary": "S"},
            "source_url": "https://feed.example/rss",
            "feed_title": "Feed",
        },
        "crypto",
    )

    assert len(dto.source_id) == 32
    assert dto.source_type == "news"


def test_onchain_normalize_whale_payload():
    collector = OnchainCollector()
    dto = collector.normalize(
        {
            "provider": "whale_alert",
            "event": {"id": "evt-1", "amount": 1000000, "symbol": "BTC", "transaction_id": "abc"},
        },
        "crypto",
    )

    assert dto.source_type == "onchain"
    assert "Whale transfer detected" in dto.content


def test_arxiv_normalize_payload():
    collector = ArxivCollector()
    dto = collector.normalize(
        {
            "entry": {
                "id": "http://arxiv.org/abs/2401.00001",
                "title": "Agentic LLM Systems",
                "summary": "A practical benchmark.",
                "authors": [{"name": "Alice"}, {"name": "Bob"}],
                "tags": [{"term": "cs.AI"}],
                "link": "https://arxiv.org/abs/2401.00001",
            }
        },
        "ai_ml",
    )

    assert dto.source_type == "arxiv"
    assert dto.source_id == "2401.00001"
    assert "Agentic LLM Systems" in dto.content


def test_github_normalize_payload():
    collector = GitHubCollector()
    dto = collector.normalize(
        {
            "repo": {
                "full_name": "example/agent-framework",
                "description": "Agent orchestration toolkit",
                "owner": {"login": "example"},
                "html_url": "https://github.com/example/agent-framework",
                "stargazers_count": 1200,
                "forks_count": 210,
                "open_issues_count": 12,
                "language": "Python",
                "topics": ["llm", "agent"],
                "updated_at": "2026-02-15T00:00:00Z",
                "pushed_at": "2026-02-15T00:00:00Z",
            }
        },
        "ai_ml",
    )

    assert dto.source_type == "github"
    assert dto.source_id == "example/agent-framework"
    assert dto.raw_metadata["stargazers_count"] == 1200
