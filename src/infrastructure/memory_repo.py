import uuid
from ..domain.entities import Sprite
from ..domain.ports import SpriteRepository


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
