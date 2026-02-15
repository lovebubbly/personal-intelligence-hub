from intel_hub.domains.base import BaseDomainConfig


class DomainRegistry:
    def __init__(self) -> None:
        self._configs: dict[str, BaseDomainConfig] = {}

    def register(self, config: BaseDomainConfig) -> None:
        self._configs[config.id] = config

    def get(self, domain_id: str) -> BaseDomainConfig:
        if domain_id not in self._configs:
            raise KeyError(f"Unknown domain_id: {domain_id}")
        return self._configs[domain_id]

    def list_active(self) -> list[BaseDomainConfig]:
        return list(self._configs.values())


_registry_singleton: DomainRegistry | None = None


def get_domain_registry() -> DomainRegistry:
    global _registry_singleton
    if _registry_singleton is None:
        from intel_hub.domains.ai_ml.config import AI_ML_DOMAIN_CONFIG
        from intel_hub.domains.crypto.config import CRYPTO_DOMAIN_CONFIG

        _registry_singleton = DomainRegistry()
        _registry_singleton.register(CRYPTO_DOMAIN_CONFIG)
        _registry_singleton.register(AI_ML_DOMAIN_CONFIG)
    return _registry_singleton
