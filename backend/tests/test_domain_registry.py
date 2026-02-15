from intel_hub.domains.registry import get_domain_registry


def test_registry_has_crypto_domain():
    registry = get_domain_registry()
    cfg = registry.get("crypto")

    assert cfg.id == "crypto"
    assert "BTC" in cfg.topics
    assert "TwitterCollector" in cfg.collectors


def test_registry_has_ai_ml_domain():
    registry = get_domain_registry()
    cfg = registry.get("ai_ml")

    assert cfg.id == "ai_ml"
    assert "LLM" in cfg.topics
    assert "ArxivCollector" in cfg.collectors
