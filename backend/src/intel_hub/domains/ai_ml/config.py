from intel_hub.domains.ai_ml.action_signals import AI_ML_ACTION_SIGNALS
from intel_hub.domains.ai_ml.kol_list import AI_ML_KOL_LIST
from intel_hub.domains.ai_ml.prompts import AI_ML_ANALYZER_PROMPT, AI_ML_NOISE_FILTER_PROMPT
from intel_hub.domains.base import BaseDomainConfig

AI_ML_DOMAIN_CONFIG = BaseDomainConfig(
    id="ai_ml",
    display_name="🤖 AI/ML",
    description="AI/ML research and product intelligence",
    kol_list=AI_ML_KOL_LIST,
    rss_sources=[
        "https://openai.com/news/rss.xml",
        "https://www.anthropic.com/news/rss.xml",
        "https://deepmind.google/blog/rss.xml",
        "https://huggingface.co/blog/feed.xml",
        "https://thegradient.pub/rss/",
    ],
    collectors=["TwitterCollector", "RSSCollector", "ArxivCollector", "GitHubCollector"],
    noise_filter_prompt=AI_ML_NOISE_FILTER_PROMPT,
    analyzer_prompt=AI_ML_ANALYZER_PROMPT,
    action_signals=AI_ML_ACTION_SIGNALS,
    categories=[
        "model_release",
        "paper",
        "tool",
        "framework",
        "regulation",
        "benchmark",
        "dataset",
        "open_source",
        "other",
    ],
    topics=["LLM", "Agent", "Vision", "Multimodal", "Safety", "Infra", "Open Source"],
)
