import uuid

from ..domain.entities import Sprite
from ..domain.repositories import SpriteRepository, StorageInterface


class InMemorySpriteRepository(SpriteRepository):
    def __init__(self):
        self._sprites: dict[uuid.UUID, Sprite] = {}

    async def add(self, sprite: Sprite) -> Sprite:
        self._sprites[sprite.id] = sprite
        return sprite

    async def get(self, sprite_id: uuid.UUID) -> Sprite | None:
        return self._sprites.get(sprite_id)

    async def list(self, limit: int = 10, offset: int = 0) -> list[Sprite]:
        all_sprites = list(self._sprites.values())
        return all_sprites[offset : offset + limit]

    async def save(self, sprite: Sprite) -> Sprite:
        self._sprites[sprite.id] = sprite
        return sprite


class LocalStorageService(StorageInterface):
    def __init__(self, base_path: str = "/tmp/spriter_uploads"):
        self.base_path = base_path
        # Ensure dir exists
        import os

        os.makedirs(base_path, exist_ok=True)

    async def upload(self, file_content: bytes, filename: str) -> str:
        import os

        full_path = os.path.join(self.base_path, filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "wb") as f:
            f.write(file_content)
        return f"file://{full_path}"
