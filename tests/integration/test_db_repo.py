import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.domain.entities import Sprite
from src.infrastructure.database import Base
from src.infrastructure.repositories import SqlAlchemySpriteRepository

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.mark.asyncio
async def test_sqlalchemy_repo(db_session):
    repo = SqlAlchemySpriteRepository(db_session)

    # Create
    sprite = Sprite(name="Integration Test Sprite", author_id="tester")
    saved_sprite = await repo.add(sprite)
    assert saved_sprite.id == sprite.id

    # Get
    fetched_sprite = await repo.get(sprite.id)
    assert fetched_sprite is not None
    assert fetched_sprite.name == "Integration Test Sprite"

    # List
    sprites = await repo.list()
    assert len(sprites) == 1
    assert sprites[0].id == sprite.id
