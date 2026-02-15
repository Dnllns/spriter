import pytest
import shutil
from pathlib import Path
from src.infrastructure.storage import FileSystemStorageAdapter


@pytest.fixture
def temp_storage_path(tmp_path):
    storage_path = tmp_path / "storage"
    yield str(storage_path)
    if storage_path.exists():
        shutil.rmtree(storage_path)


@pytest.mark.asyncio
async def test_save_file(temp_storage_path):
    adapter = FileSystemStorageAdapter(base_path=temp_storage_path)
    content = b"test content"
    path = "folder/test.png"

    saved_path = await adapter.save(content, path)
    assert saved_path == path

    # Verify file exists
    full_path = Path(temp_storage_path) / path
    assert full_path.exists()
    assert full_path.read_bytes() == content


@pytest.mark.asyncio
async def test_get_file(temp_storage_path):
    adapter = FileSystemStorageAdapter(base_path=temp_storage_path)
    content = b"data"
    path = "data.bin"

    # Create manually
    full_path = Path(temp_storage_path) / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_bytes(content)

    retrieved = await adapter.get(path)
    assert retrieved == content


@pytest.mark.asyncio
async def test_get_file_not_found(temp_storage_path):
    adapter = FileSystemStorageAdapter(base_path=temp_storage_path)
    retrieved = await adapter.get("nonexistent.txt")
    assert retrieved is None


@pytest.mark.asyncio
async def test_delete_file(temp_storage_path):
    adapter = FileSystemStorageAdapter(base_path=temp_storage_path)
    path = "todelete.txt"
    full_path = Path(temp_storage_path) / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    full_path.write_text("delete me")

    assert await adapter.delete(path) is True
    assert not full_path.exists()

    # Delete non-existent
    assert await adapter.delete("nothing") is False
