import json
from datetime import date
from decimal import Decimal

import httpx
import structlog

from intel_hub.config import get_settings
from intel_hub.db.repository import HubRepository
from intel_hub.services.retry import retry_external_call

logger = structlog.get_logger(__name__)


class GeminiClient:
    def __init__(self, repository: HubRepository):
        self.settings = get_settings()
        self.repo = repository
        self.client = httpx.Client(timeout=40.0)

    @retry_external_call
    def generate_json(self, prompt: str) -> dict:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-2.0-flash:generateContent?key={self.settings.google_ai_api_key}"
        )
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"},
        }
        response = self.client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        text = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "{}")
        )
        parsed = json.loads(text)

        usage = data.get("usageMetadata", {})
        self.repo.record_model_usage(
            usage_date=date.today(),
            model="gemini-2.0-flash",
            tokens_in=int(usage.get("promptTokenCount", 0)),
            tokens_out=int(usage.get("candidatesTokenCount", 0)),
            cost_estimate=Decimal("0"),
        )
        return parsed


class ClaudeClient:
    def __init__(self, repository: HubRepository):
        self.settings = get_settings()
        self.repo = repository
        self.client = httpx.Client(timeout=45.0)

    @retry_external_call
    def generate_json(self, prompt: str) -> dict:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.settings.anthropic_api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload = {
            "model": "claude-3-5-sonnet-latest",
            "max_tokens": 800,
            "system": "Respond with strict JSON only.",
            "messages": [{"role": "user", "content": prompt}],
        }
        response = self.client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        text = data.get("content", [{}])[0].get("text", "{}")
        parsed = json.loads(text)

        usage = data.get("usage", {})
        self.repo.record_model_usage(
            usage_date=date.today(),
            model="claude-3-5-sonnet-latest",
            tokens_in=int(usage.get("input_tokens", 0)),
            tokens_out=int(usage.get("output_tokens", 0)),
            cost_estimate=Decimal("0"),
        )
        return parsed
