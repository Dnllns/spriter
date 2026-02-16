import uuid
from abc import ABC, abstractmethod

from .entities import Sprite, User


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


class StoragePort(ABC):
    @abstractmethod
    async def save(self, file_content: bytes, path: str) -> str:
        """
        Save binary content to the storage system.
        :param file_content: The binary data to store.
        :param path: The relative path or key (e.g., 'sprites/123/v1.png').
        :return: A public or internal URL/URI to access the file.
        """
        pass

    @abstractmethod
    async def get(self, path: str) -> bytes | None:
        """
        Retrieve binary content from storage.
        :param path: The relative path or key.
        :return: The binary content or None if not found.
        """
        pass

    @abstractmethod
    async def delete(self, path: str) -> bool:
        """
        Delete a file from storage.
        """
        pass


class AuthenticatorPort(ABC):
    @abstractmethod
    async def authenticate(self, token: str) -> User:
        """
        Verifies the token and returns the authenticated user.
        Raises exception if invalid.
        """
        pass
