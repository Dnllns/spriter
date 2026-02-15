from fastapi import Depends
from sqlalchemy.orm import Session

from .application.services import SpriteService
from .config import settings
from .domain.ports import SpriteRepository, StoragePort
from .infrastructure.database import get_db
from .infrastructure.repositories import SqlAlchemySpriteRepository
from .infrastructure.storage import FileSystemStorageAdapter

# Using the new aiofiles-based adapter
_storage = FileSystemStorageAdapter(base_path=settings.STORAGE_PATH)


def get_storage() -> StoragePort:
    return _storage


def get_repository(db: Session = Depends(get_db)) -> SpriteRepository:
    return SqlAlchemySpriteRepository(db)


def get_service(
    repo: SpriteRepository = Depends(get_repository),
    storage: StoragePort = Depends(get_storage),
) -> SpriteService:
    return SpriteService(repo, storage)
