import pytest
import uuid
from httpx import AsyncClient, ASGITransport

from src.domain.entities import Sprite
from src.infrastructure.memory_repo import InMemorySpriteRepository
from src.main import app
from src.dependencies import get_repository


@pytest.fixture
def memory_repo():
    repo = InMemorySpriteRepository()
    return repo


@pytest.fixture
def override_repo(memory_repo):
    app.dependency_overrides[get_repository] = lambda: memory_repo
    yield
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_track_sprite_play(override_repo, memory_repo):
    # Setup test sprite
    sprite_id = uuid.uuid4()
    sprite = Sprite(id=sprite_id, name="Test Sprite", author_id="author1")
    await memory_repo.add(sprite)

    # Ping analytics
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(f"/api/v1/analytics/sprites/{sprite_id}/play")

    assert response.status_code == 202
    assert response.json()["status"] == "accepted"

    # AsyncClient with ASGITransport executes BackgroundTasks before returning the response
    # so we can safely check the result immediately.
    updated_sprite = await memory_repo.get(sprite_id)
    assert updated_sprite.play_count == 1
