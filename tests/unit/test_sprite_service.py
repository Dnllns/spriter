import pytest
from src.application.dto import CreateSpriteRequest
from src.application.services import SpriteService
from src.infrastructure.memory_repo import InMemorySpriteRepository
from src.domain.ports import StoragePort


class MockStorage(StoragePort):
    async def save(self, content: bytes, path: str) -> str:
        return path

    async def get(self, path: str) -> bytes | None:
        return None

    async def delete(self, path: str) -> bool:
        return True


@pytest.mark.asyncio
async def test_create_sprite():
    repo = InMemorySpriteRepository()
    storage = MockStorage()
    service = SpriteService(repo, storage)

    request = CreateSpriteRequest(name="Test Sprite", tags=["hero", "rpg"])
    sprite = await service.create_new_sprite(request, author_id="user_123")

    assert sprite.name == "Test Sprite"
    assert sprite.author_id == "user_123"
    assert "hero" in sprite.tags
    assert sprite.status == "draft"

    saved_sprite = await repo.get(sprite.id)
    assert saved_sprite is not None
    assert saved_sprite.id == sprite.id
