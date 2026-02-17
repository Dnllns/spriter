import io

import pytest
from PIL import Image

from src.application.dto import AddVersionRequest
from src.application.services import SpriteService
from src.domain.entities import Animation, Frame
from src.domain.ports import StoragePort
from src.infrastructure.memory_repo import InMemorySpriteRepository


class MockStorage(StoragePort):
    def __init__(self):
        self.files = {}

    async def save(self, content: bytes, path: str) -> str:
        self.files[path] = content
        return path

    async def get(self, path: str) -> bytes | None:
        return self.files.get(path)

    async def delete(self, path: str) -> bool:
        if path in self.files:
            del self.files[path]
            return True
        return False


@pytest.mark.asyncio
async def test_add_sprite_version_with_slicing():
    repo = InMemorySpriteRepository()
    storage = MockStorage()
    service = SpriteService(repo, storage)

    # 1. Create Sprite
    from src.application.dto import CreateSpriteRequest

    sprite = await service.create_new_sprite(
        CreateSpriteRequest(name="Walker"), author_id="dev"
    )

    # 2. Create a mock spritesheet (64x32 -> two 32x32 frames)
    img = Image.new("RGBA", (64, 32), (255, 0, 0, 255))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    file_content = img_byte_arr.getvalue()

    request = AddVersionRequest(
        metadata={"frame_w": 32, "frame_h": 32},
        changelog="Added walk animation",
        animations=[
            Animation(
                name="walk",
                fps=8,
                frames=[
                    Frame(index=0),
                    Frame(index=1),
                ],
                loop=True,
            )
        ],
    )

    # 3. Add version
    version = await service.add_sprite_version(sprite.id, file_content, request)

    # 4. Assertions
    assert version is not None
    assert len(sprite.versions) == 1

    # Check if frames were saved individually
    frame0_path = f"sprites/{sprite.id}/v1/frames/f0.png"
    frame1_path = f"sprites/{sprite.id}/v1/frames/f1.png"
    assert frame0_path in storage.files
    assert frame1_path in storage.files

    # Check if animations were updated with image locations
    walk_anim = sprite.versions[0].animations[0]
    assert walk_anim.frames[0].image_location == frame0_path
    assert walk_anim.frames[1].image_location == frame1_path
