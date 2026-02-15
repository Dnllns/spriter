import uuid
from abc import ABC, abstractmethod

from .entities import Sprite


class SpriteRepository(ABC):
    @abstractmethod
    async def add(self, sprite: Sprite) -> Sprite:
        pass

    @abstractmethod
    async def get(self, sprite_id: uuid.UUID) -> Sprite | None:
        pass

    @abstractmethod
    async def list(self, limit: int = 10, offset: int = 0) -> list[Sprite]:
        pass

    @abstractmethod
    async def save(self, sprite: Sprite) -> Sprite:
        """Update existing or save new"""
        pass


class StorageInterface(ABC):
    @abstractmethod
    async def upload(self, file_content: bytes, filename: str) -> str:
        """Uploads file content and returns publicly accessible URL."""
        pass
