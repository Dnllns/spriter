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


class User(BaseModel):
    id: str
    email: str | None = None
    username: str | None = None


class Frame(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    index: int
    duration_ms: int = 100  # Default 100ms per frame
    image_location: str | None = None  # Could be path or internal reference
    metadata: dict = Field(default_factory=dict)


class Animation(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    type: AnimationType = AnimationType.CUSTOM
    fps: int = 10
    frames: list[Frame] = Field(default_factory=list)
    loop: bool = True


class SpriteVersion(BaseModel):
    version: int = 1
    image_url: str
    metadata: dict = Field(default_factory=dict)
    animations: list[Animation] = Field(
        default_factory=list
    )  # Added animations support
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
        self,
        image_url: str,
        metadata: dict,
        changelog: str | None = None,
        animations: list[Animation] | None = None,
    ) -> SpriteVersion:
        """Adds a new version to the sprite."""
        new_version_num = len(self.versions) + 1
        new_version = SpriteVersion(
            version=new_version_num,
            image_url=image_url,
            metadata=metadata,
            changelog=changelog,
            animations=animations or [],
        )
        self.versions.append(new_version)
        self.updated_at = datetime.now(UTC)
        return new_version
