from pydantic import BaseModel, Field, field_validator


class NoiseFilterResult(BaseModel):
    is_signal: bool
    noise_reason: str | None = None
    importance_score: int = Field(ge=1, le=10)
    related_topics: list[str] = Field(default_factory=list)
    category: str
    context_summary: str


class AnalyzerResult(BaseModel):
    sentiment_score: int = Field(ge=-100, le=100)
    action_signal: str
    analysis: str

    @field_validator("action_signal")
    @classmethod
    def validate_action_signal(cls, value: str) -> str:
        allowed = {
            "opportunity",
            "watch",
            "risk",
            "neutral",
            "apply",
            "learn",
            "paradigm_shift",
        }
        if value not in allowed:
            raise ValueError(f"action_signal must be one of {sorted(allowed)}")
        return value


class DigestResult(BaseModel):
    summary: str
    detailed_analysis: str
