import os
import aiofiles
from ..domain.ports import StoragePort
from ..config import settings


class FileSystemStorageAdapter(StoragePort):
    def __init__(self, base_path: str = settings.STORAGE_PATH):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
        # Ensure imports work (config import may not be available yet if dependency order is broken)

    async def save(self, file_content: bytes, path: str) -> str:
        """
        Saves binary content to local filesystem asynchronously.
        Path is relative to base_path. e.g. 'sprites/123/v1.png'
        """
        full_path = os.path.join(self.base_path, path)
        dir_name = os.path.dirname(full_path)

        # Ensure directories exist (blocking op, but minimal impact on directories)
        os.makedirs(dir_name, exist_ok=True)

        # Async write
        async with aiofiles.open(full_path, mode="wb") as f:
            await f.write(file_content)

        # Return local file URI or relative path
        # For simplicity, returning the relative path which can be served
        return path

    async def get(self, path: str) -> bytes | None:
        full_path = os.path.join(self.base_path, path)
        if not os.path.exists(full_path):
            return None

        async with aiofiles.open(full_path, mode="rb") as f:
            return await f.read()

    async def delete(self, path: str) -> bool:
        """
        Deletes file if exists.
        Warning: os.remove is blocking. Aiofiles doesn't wrap remove.
        For rigorous async, run in executor. For now, it's acceptable for MVPs.
        """
        full_path = os.path.join(self.base_path, path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False
