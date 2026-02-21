import uuid

import structlog

from ..domain.ports import SpriteRepository

logger = structlog.get_logger(__name__)


class AnalyticsService:
    """Service to handle tracking and analytics for sprites."""

    def __init__(self, repo: SpriteRepository):
        self.repo = repo

    async def register_play(self, sprite_id: uuid.UUID) -> None:
        """
        Registers a play event for the given sprite.
        Incrementing the counter asynchronously.
        """
        logger.info("analytics_play_registered", sprite_id=str(sprite_id))
        await self.repo.increment_play_count(sprite_id)
