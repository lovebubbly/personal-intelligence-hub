from datetime import UTC, datetime, timedelta

import httpx
import structlog

from intel_hub.collectors.base import BaseCollector, RawItemDTO
from intel_hub.config import get_settings
from intel_hub.services.retry import retry_external_call

logger = structlog.get_logger(__name__)


class GitHubCollector(BaseCollector):
    source_type = "github"

    search_url = "https://api.github.com/search/repositories"

    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = httpx.Client(timeout=25.0)

    @retry_external_call
    def _search_repositories(self) -> list[dict]:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.settings.github_token:
            headers["Authorization"] = f"Bearer {self.settings.github_token}"

        params = {
            "q": "(topic:machine-learning OR topic:llm) language:python stars:>500",
            "sort": "updated",
            "order": "desc",
            "per_page": 20,
        }
        response = self.client.get(self.search_url, headers=headers, params=params)
        response.raise_for_status()
        payload = response.json()
        return payload.get("items", [])

    def collect(self, domain_id: str, since: datetime | None = None) -> list[RawItemDTO]:
        if domain_id != "ai_ml":
            return []

        since_dt = since or datetime.now(UTC) - timedelta(hours=6)
        try:
            repos = self._search_repositories()
        except Exception as exc:
            logger.warning("github_collect_failed", domain=domain_id, error=str(exc))
            return []

        items: list[RawItemDTO] = []
        for repo in repos:
            pushed_at = repo.get("pushed_at")
            if pushed_at:
                pushed_dt = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
                if pushed_dt < since_dt:
                    continue
            items.append(self.normalize({"repo": repo}, domain_id))
        return items

    def normalize(self, payload: dict, domain_id: str) -> RawItemDTO:
        repo = payload["repo"]
        source_id = repo.get("full_name")
        description = repo.get("description") or ""
        content = f"{repo.get('full_name')}\n\n{description}".strip()

        return RawItemDTO(
            domain_id=domain_id,
            source_type=self.source_type,
            source_id=source_id,
            author=repo.get("owner", {}).get("login"),
            content=content,
            url=repo.get("html_url"),
            raw_metadata={
                "stargazers_count": repo.get("stargazers_count", 0),
                "forks_count": repo.get("forks_count", 0),
                "open_issues_count": repo.get("open_issues_count", 0),
                "language": repo.get("language"),
                "topics": repo.get("topics", []),
                "updated_at": repo.get("updated_at"),
                "pushed_at": repo.get("pushed_at"),
            },
            collected_at=datetime.now(UTC),
        )
