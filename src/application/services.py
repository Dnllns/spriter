import io
import uuid

from PIL import Image

from ..domain.entities import Sprite, SpriteVersion
from ..domain.exceptions import SpriteNotFoundError
from ..domain.ports import SpriteRepository, StoragePort
from .dto import AddVersionRequest, CreateSpriteRequest, UpdateAnimationsRequest


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
            is_public=request.is_public,
        )
        await self.repo.add(sprite)
        return sprite

    async def add_sprite_version(
        self, sprite_id: uuid.UUID, file_content: bytes, request: AddVersionRequest
    ) -> SpriteVersion | None:
        sprite = await self.repo.get(sprite_id)
        if not sprite:
            raise SpriteNotFoundError(sprite_id)

        # 1. Save original bundle (optional, but kept for context/fallback)
        version_num = len(sprite.versions) + 1
        bundle_path = f"sprites/{sprite_id}/v{version_num}/bundle.png"
        bundle_url = await self.storage.save(file_content, bundle_path)

        # 2. Check for slicing metadata
        frame_w = request.metadata.get("frame_w")
        frame_h = request.metadata.get("frame_h")

        if frame_w and frame_h:
            img = Image.open(io.BytesIO(file_content))
            sheet_w, sheet_h = img.size

            # Map of frame index to its URL
            frame_urls = {}

            cols = sheet_w // frame_w
            rows = sheet_h // frame_h

            for row in range(rows):
                for col in range(cols):
                    idx = row * cols + col
                    left = col * frame_w
                    top = row * frame_h
                    right = left + frame_w
                    bottom = top + frame_h

                    # Slice
                    frame_img = img.crop((left, top, right, bottom))

                    # Convert to bytes
                    frame_bytes = io.BytesIO()
                    frame_img.save(frame_bytes, format="PNG")

                    # Save individual frame
                    frame_path = f"sprites/{sprite_id}/v{version_num}/frames/f{idx}.png"
                    frame_url = await self.storage.save(
                        frame_bytes.getvalue(), frame_path
                    )
                    frame_urls[idx] = frame_url

            # 3. Update animations to use individual frame URLs
            for anim in request.animations:
                for frame in anim.frames:
                    if frame.index in frame_urls:
                        frame.image_location = frame_urls[frame.index]

        version = sprite.add_version(
            image_url=bundle_url,
            metadata=request.metadata,
            changelog=request.changelog,
            animations=request.animations,
        )

        await self.repo.save(sprite)
        return version

    async def get_sprite(self, sprite_id: uuid.UUID) -> Sprite:
        sprite = await self.repo.get(sprite_id)
        if not sprite:
            raise SpriteNotFoundError(sprite_id)
        return sprite

    async def list_sprites(
        self, limit: int = 10, offset: int = 0, only_public: bool = False
    ) -> list[Sprite]:
        return await self.repo.list(
            limit, offset, is_public=True if only_public else None
        )

    async def update_sprite_animations(
        self, sprite_id: uuid.UUID, request: UpdateAnimationsRequest
    ) -> Sprite:
        sprite = await self.repo.get(sprite_id)
        if not sprite:
            raise SpriteNotFoundError(sprite_id)

        if not sprite.versions:
            # Cannot update animations if no version exists
            raise ValueError("Sprite has no versions to update")

        # Update the latest version's animations
        latest_version = sprite.versions[-1]
        latest_version.animations = request.animations

        await self.repo.save(sprite)
        return sprite
