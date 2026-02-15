from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Personal Intelligence Hub API"
    app_env: Literal["local", "dev", "prod", "test"] = "local"
    app_timezone: str = "Asia/Seoul"

    database_url: str = Field(default="postgresql+psycopg://postgres:postgres@localhost:5432/intel_hub")
    redis_url: str = Field(default="redis://localhost:6379/0")

    twitter_bearer_token: str = ""
    anthropic_api_key: str = ""
    google_ai_api_key: str = ""
    supabase_url: str = ""
    supabase_key: str = ""
    telegram_bot_token: str = ""
    github_token: str = ""
    whale_alert_api_key: str = ""
    dune_api_key: str = ""

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    socket_namespace: str = "/feed"
    redis_stream_raw: str = "stream:raw_items"
    redis_stream_analyzed: str = "stream:analyzed_items"
    redis_stream_failed_jobs: str = "stream:failed_jobs"
    redis_consumer_group_raw: str = "noise_filter_group"
    redis_consumer_group_analyzed: str = "analyzer_group"

    importance_alert_threshold: int = 8
    risk_alert_threshold: int = 7

    daily_digest_hour_kst: int = 9

    def validate_required(self) -> None:
        required = {
            "TWITTER_BEARER_TOKEN": self.twitter_bearer_token,
            "ANTHROPIC_API_KEY": self.anthropic_api_key,
            "GOOGLE_AI_API_KEY": self.google_ai_api_key,
            "SUPABASE_URL": self.supabase_url,
            "SUPABASE_KEY": self.supabase_key,
            "REDIS_URL": self.redis_url,
            "TELEGRAM_BOT_TOKEN": self.telegram_bot_token,
        }
        missing = [key for key, value in required.items() if not value]
        if missing:
            missing_list = ", ".join(missing)
            raise RuntimeError(f"Missing required environment variables: {missing_list}")


@lru_cache
def get_settings() -> Settings:
    return Settings()
