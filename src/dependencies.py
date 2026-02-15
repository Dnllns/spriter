from fastapi import Depends
from sqlalchemy.orm import Session

from .application.services import SpriteService
from .config import settings
from .domain.repositories import SpriteRepository, StorageInterface
from .infrastructure.database import get_db
from .infrastructure.memory_repo import LocalStorageService
from .infrastructure.repositories import SqlAlchemySpriteRepository

# Storage remains local for now, but could be switched based on settings
_storage = LocalStorageService(base_path=settings.STORAGE_PATH)


def get_storage() -> StorageInterface:
    return _storage


def get_repository(db: Session = Depends(get_db)) -> SpriteRepository:
    return SqlAlchemySpriteRepository(db)


def get_service(
    repo: SpriteRepository = Depends(get_repository),
    storage: StorageInterface = Depends(get_storage),
) -> SpriteService:
    return SpriteService(repo, storage)
