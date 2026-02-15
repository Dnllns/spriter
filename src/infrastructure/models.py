import uuid
from datetime import UTC, datetime

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy import (
    Enum as SAEnum,
)
from sqlalchemy.orm import relationship

from ..domain.entities import SpriteStatus
from .database import Base


class SpriteModel(Base):
    __tablename__ = "sprites"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    author_id = Column(String, nullable=False)
    status = Column(SAEnum(SpriteStatus), default=SpriteStatus.DRAFT)
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    versions = relationship("SpriteVersionModel", back_populates="sprite")


class SpriteVersionModel(Base):
    __tablename__ = "sprite_versions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sprite_id = Column(String, ForeignKey("sprites.id"))
    version_number = Column(Integer, nullable=False)
    image_url = Column(String, nullable=False)
    metadata_json = Column(JSON, default=dict)
    changelog = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    sprite = relationship("SpriteModel", back_populates="versions")
