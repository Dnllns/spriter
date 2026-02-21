import uuid

from fastapi import APIRouter, BackgroundTasks, Depends

from ..application.analytics import AnalyticsService
from ..dependencies import get_analytics_service

router = APIRouter(tags=["Analytics"])


@router.post("/analytics/sprites/{sprite_id}/play", status_code=202)
async def track_sprite_play(
    sprite_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    analytics_svc: AnalyticsService = Depends(get_analytics_service),
):
    """
    Tracks a 'play' event for a specific sprite.
    Uses BackgroundTasks so the response is fast and non-blocking.
    """
    background_tasks.add_task(analytics_svc.register_play, sprite_id)
    return {"status": "accepted"}
