import uuid
from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class SpriteStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class AnimationType(StrEnum):
    IDLE = "idle"
    RUN = "run"
    JUMP = "jump"
    ATTACK = "attack"
    CUSTOM = "custom"


class SpriteVersion(BaseModel):
    version: int = 1
    image_url: str
    metadata: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    changelog: str | None = None


class Sprite(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    description: str | None = None
    author_id: str
    tags: list[str] = Field(default_factory=list)
    status: SpriteStatus = SpriteStatus.DRAFT
    versions: list[SpriteVersion] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def add_version(
        self, image_url: str, metadata: dict, changelog: str | None = None
    ) -> SpriteVersion:
        """Adds a new version to the sprite."""
        new_version_num = len(self.versions) + 1
        new_version = SpriteVersion(
            version=new_version_num,
            image_url=image_url,
            metadata=metadata,
            changelog=changelog,
        )
        self.versions.append(new_version)
        self.updated_at = datetime.now(UTC)
        return new_version
