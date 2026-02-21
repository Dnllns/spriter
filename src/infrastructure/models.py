import uuid
from datetime import UTC, datetime
from typing import List, Optional

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy import (
    Enum as SAEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..domain.entities import SpriteStatus
from .database import Base


class SpriteModel(Base):
    __tablename__ = "sprites"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    author_id: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[SpriteStatus] = mapped_column(
        SAEnum(SpriteStatus), default=SpriteStatus.DRAFT
    )
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, server_default="1")
    tags: Mapped[List[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    versions: Mapped[List["SpriteVersionModel"]] = relationship(
        "SpriteVersionModel", back_populates="sprite"
    )


class SpriteVersionModel(Base):
    __tablename__ = "sprite_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sprite_id: Mapped[str] = mapped_column(String, ForeignKey("sprites.id"))
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    animations_json: Mapped[List[dict]] = mapped_column(JSON, default=list)
    changelog: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC)
    )

    sprite: Mapped["SpriteModel"] = relationship(
        "SpriteModel", back_populates="versions"
    )
