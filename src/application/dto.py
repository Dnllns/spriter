from pydantic import BaseModel

from ..domain.entities import Animation


class CreateSpriteRequest(BaseModel):
    name: str
    description: str | None = None
    tags: list[str] = []
    is_public: bool = True


class AddVersionRequest(BaseModel):
    changelog: str | None = None
    metadata: dict = {}
    animations: list[Animation] = []
    # File content is handled separately in the service via bytes
