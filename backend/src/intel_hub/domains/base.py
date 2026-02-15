from dataclasses import dataclass


@dataclass(frozen=True)
class ActionSignalDefinition:
    name: str
    icon: str
    description: str


@dataclass(frozen=True)
class BaseDomainConfig:
    id: str
    display_name: str
    description: str
    kol_list: list[dict]
    rss_sources: list[str]
    collectors: list[str]
    noise_filter_prompt: str
    analyzer_prompt: str
    action_signals: dict[str, ActionSignalDefinition]
    categories: list[str]
    topics: list[str]
