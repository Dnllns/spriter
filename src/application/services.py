import uuid

from ..domain.entities import Sprite, SpriteVersion
from ..domain.ports import SpriteRepository, StoragePort
from .dto import AddVersionRequest, CreateSpriteRequest


class SpriteService:
    def __init__(self, repo: SpriteRepository, storage: StoragePort):
        self.repo = repo
        self.storage = storage

    async def create_new_sprite(
        self, request: CreateSpriteRequest, author_id: str
    ) -> Sprite:
        sprite = Sprite(
            name=request.name,
            description=request.description,
            tags=request.tags,
            author_id=author_id,
        )
        await self.repo.add(sprite)
        return sprite

    async def add_sprite_version(
        self, sprite_id: uuid.UUID, file_content: bytes, request: AddVersionRequest
    ) -> SpriteVersion | None:
        sprite = await self.repo.get(sprite_id)
        if not sprite:
            return None

        # Upload file (simplified path logic)
        path = f"sprites/{sprite_id}/v{len(sprite.versions) + 1}.png"
        url = await self.storage.save(file_content, path)

        version = sprite.add_version(
            image_url=url, metadata=request.metadata, changelog=request.changelog
        )

        await self.repo.save(sprite)
        return version

    async def get_sprite(self, sprite_id: uuid.UUID) -> Sprite | None:
        return await self.repo.get(sprite_id)

    async def list_sprites(self, limit: int = 10, offset: int = 0) -> list[Sprite]:
        return await self.repo.list(limit, offset)
