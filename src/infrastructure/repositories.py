import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..domain.entities import Sprite, SpriteVersion
from ..domain.ports import SpriteRepository
from .models import SpriteModel, SpriteVersionModel


class SqlAlchemySpriteRepository(SpriteRepository):
    def __init__(self, db: Session):
        self.db = db

    async def add(self, sprite: Sprite) -> Sprite:
        db_sprite = SpriteModel(
            id=str(sprite.id),
            name=sprite.name,
            description=sprite.description,
            author_id=sprite.author_id,
            status=sprite.status,
            tags=sprite.tags,
            created_at=sprite.created_at,
            updated_at=sprite.updated_at,
        )
        self.db.add(db_sprite)
        self.db.commit()
        self.db.refresh(db_sprite)
        return sprite

    async def get(self, sprite_id: uuid.UUID) -> Sprite | None:
        db_sprite = (
            self.db.query(SpriteModel).filter(SpriteModel.id == str(sprite_id)).first()
        )
        if not db_sprite:
            return None
        return self._to_domain(db_sprite)

    async def list(self, limit: int = 10, offset: int = 0) -> list[Sprite]:
        stmt = select(SpriteModel).offset(offset).limit(limit)
        result = self.db.execute(stmt).scalars().all()
        return [self._to_domain(s) for s in result]

    async def save(self, sprite: Sprite) -> Sprite:
        # A simple approach: update fields on the existing model
        db_sprite = (
            self.db.query(SpriteModel).filter(SpriteModel.id == str(sprite.id)).first()
        )
        if db_sprite:
            db_sprite.name = sprite.name
            db_sprite.description = sprite.description
            db_sprite.updated_at = sprite.updated_at
            db_sprite.tags = sprite.tags

            # Sync versions - rudimentary approach: add missing versions
            # In a real app, careful diffing is needed
            current_version_nums = {v.version_number for v in db_sprite.versions}
            for v in sprite.versions:
                if v.version not in current_version_nums:
                    new_version_model = SpriteVersionModel(
                        sprite_id=str(sprite.id),
                        version_number=v.version,
                        image_url=v.image_url,
                        metadata_json=v.metadata,
                        animations_json=[
                            a.model_dump(mode="json") for a in v.animations
                        ],
                        changelog=v.changelog,
                        created_at=v.created_at,
                    )
                    self.db.add(new_version_model)

            self.db.commit()
            self.db.refresh(db_sprite)
        return sprite

    def _to_domain(self, model: SpriteModel) -> Sprite:
        domain_versions = [
            SpriteVersion(
                version=v.version_number,
                image_url=v.image_url,
                metadata=v.metadata_json,
                animations=v.animations_json,
                created_at=v.created_at,
                changelog=v.changelog,
            )
            for v in model.versions
        ]
        # Sort versions by number
        domain_versions.sort(key=lambda x: x.version)

        return Sprite(
            id=uuid.UUID(model.id),
            name=model.name,
            description=model.description,
            author_id=model.author_id,
            status=model.status,
            tags=model.tags if model.tags else [],
            created_at=model.created_at,
            updated_at=model.updated_at,
            versions=domain_versions,
        )
