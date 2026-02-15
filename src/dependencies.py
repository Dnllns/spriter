from fastapi import Depends

from ..application.services import SpriteService
from ..domain.repositories import SpriteRepository, StorageInterface
from ..infrastructure.memory_repo import InMemorySpriteRepository, LocalStorageService

# Singleton instance for now (in-memory)
_repo = InMemorySpriteRepository()
_storage = LocalStorageService()


def get_repository() -> SpriteRepository:
    return _repo


def get_storage() -> StorageInterface:
    return _storage


def get_service(
    repo: SpriteRepository = Depends(get_repository),
    storage: StorageInterface = Depends(get_storage),
) -> SpriteService:
    return SpriteService(repo, storage)
