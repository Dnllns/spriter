from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .application.analytics import AnalyticsService
from .application.services import SpriteService
from .config import settings
from .domain.ports import AuthenticatorPort, SpriteRepository, StoragePort, User
from .infrastructure.auth import MockAuthenticator
from .infrastructure.database import get_db
from .infrastructure.repositories import SqlAlchemySpriteRepository
from .infrastructure.storage import FileSystemStorageAdapter

# Using the new aiofiles-based adapter
_storage = FileSystemStorageAdapter(base_path=settings.STORAGE_PATH)
# For now using MockAuthenticator. In production change to OIDCAuthenticatorAdapter.
_authenticator = MockAuthenticator()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


def get_storage() -> StoragePort:
    return _storage


def get_authenticator() -> AuthenticatorPort:
    return _authenticator


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth: AuthenticatorPort = Depends(get_authenticator),
) -> User:
    if not token:
        # For development ease, we allow a bypass or default if not configured.
        # But for strict production, raise 401.
        # Let's be strict but allow a 'dev' token.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await auth.authenticate(token)


async def get_current_user_optional(
    token: str = Depends(oauth2_scheme),
    auth: AuthenticatorPort = Depends(get_authenticator),
) -> User | None:
    if not token:
        return None
    try:
        return await auth.authenticate(token)
    except Exception:
        return None


def get_repository(db: Session = Depends(get_db)) -> SpriteRepository:
    return SqlAlchemySpriteRepository(db)


def get_service(
    repo: SpriteRepository = Depends(get_repository),
    storage: StoragePort = Depends(get_storage),
) -> SpriteService:
    return SpriteService(repo, storage)


def get_analytics_service(
    repo: SpriteRepository = Depends(get_repository),
) -> AnalyticsService:
    return AnalyticsService(repo)
