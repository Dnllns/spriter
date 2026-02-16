
from src.domain.entities import Animation, AnimationType, Frame, Sprite


def test_create_sprite():
    sprite = Sprite(name="Hero", author_id="user123")
    assert sprite.versions == []
    assert sprite.status == "draft"


def test_add_version_with_metadata():
    sprite = Sprite(name="Hero", author_id="user123")
    version = sprite.add_version(
        image_url="http://example.com/sprite.png",
        metadata={"width": 32, "height": 32},
        changelog="Initial version",
    )
    assert len(sprite.versions) == 1
    assert version.version == 1
    assert version.image_url == "http://example.com/sprite.png"
    assert version.metadata["width"] == 32


def test_add_version_with_animations():
    sprite = Sprite(name="Hero", author_id="user123")

    # Create an animation
    frame1 = Frame(index=0, duration_ms=100)
    frame2 = Frame(index=1, duration_ms=100)
    animation = Animation(
        name="Idle",
        type=AnimationType.IDLE,
        fps=10,
        frames=[frame1, frame2],
    )

    version = sprite.add_version(
        image_url="http://example.com/sheet.png",
        metadata={"cols": 2, "rows": 1},
        animations=[animation],
    )

    assert len(version.animations) == 1
    assert version.animations[0].name == "Idle"
    assert len(version.animations[0].frames) == 2
    assert version.animations[0].frames[0].index == 0


def test_frame_defaults():
    frame = Frame(index=5)
    assert frame.duration_ms == 100
    assert frame.metadata == {}


def test_animation_defaults():
    anim = Animation(name="Run")
    assert anim.type == "custom"  # Default type
    assert anim.fps == 10
    assert anim.loop is True
