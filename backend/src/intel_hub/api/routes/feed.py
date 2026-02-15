from datetime import datetime

from fastapi import APIRouter, Depends, Query

from intel_hub.api.deps import get_repository_dep
from intel_hub.api.schemas import FeedItemResponse

router = APIRouter(prefix="/feed", tags=["feed"])


@router.get("", response_model=list[FeedItemResponse])
def get_feed(
    domain: str = Query("all", pattern="^(all|crypto|ai_ml)$"),
    limit: int = Query(50, ge=1, le=200),
    cursor: str | None = None,
    min_importance: int = Query(1, ge=1, le=10),
    repo=Depends(get_repository_dep),
):
    cursor_dt = None
    if cursor:
        normalized = cursor.replace("Z", "+00:00")
        cursor_dt = datetime.fromisoformat(normalized)
    rows = repo.list_feed(domain=domain, limit=limit, min_importance=min_importance, cursor=cursor_dt)
    return [FeedItemResponse(**{**row, "id": str(row["id"])}) for row in rows]
