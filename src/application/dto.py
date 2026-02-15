from pydantic import BaseModel


class CreateSpriteRequest(BaseModel):
    name: str
    description: str | None = None
    tags: list[str] = []


class AddVersionRequest(BaseModel):
    changelog: str | None = None
    metadata: dict = {}
    # File content is handled separately in the service via bytes
