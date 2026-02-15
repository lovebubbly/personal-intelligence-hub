from fastapi import APIRouter, Depends, Query

from intel_hub.api.deps import get_repository_dep
from intel_hub.api.schemas import EventResponse

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[EventResponse])
def get_events(
    domain: str = Query("all", pattern="^(all|crypto|ai_ml)$"),
    limit: int = Query(20, ge=1, le=100),
    repo=Depends(get_repository_dep),
):
    rows = repo.top_analyzed_items(min_importance=6, limit=limit)
    if domain != "all":
        rows = [row for row in rows if row["domain_id"] == domain]

    events: list[EventResponse] = []
    for row in rows:
        kind = _infer_kind(row)
        title = row.get("context_summary") or row.get("content", "")[:120]
        events.append(
            EventResponse(
                id=str(row["analyzed_item_id"]),
                domain_id=row["domain_id"],
                title=title,
                date=row["collected_at"],
                kind=kind,
            )
        )
    return events


def _infer_kind(item: dict) -> str:
    source_type = item.get("source_type")
    category = (item.get("category") or "").lower()
    if item.get("domain_id") == "crypto":
        if category in {"airdrop", "partnership", "technical"}:
            return "token_unlock"
        if category in {"regulation", "macro"}:
            return "governance"
        return "governance"

    if source_type in {"github", "arxiv"} or category in {"model_release", "paper", "framework"}:
        return "model_release"
    return "conference"
