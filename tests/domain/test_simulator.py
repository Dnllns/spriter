import pytest

from src.domain.entities import Animation, Frame
from src.domain.simulator import SimulationConfig, SimulatorService


@pytest.fixture
def mock_animation():
    fram1 = Frame(index=0, duration_ms=100)
    fram2 = Frame(index=1, duration_ms=100)
    return Animation(name="Test", frames=[fram1, fram2], loop=True)


def test_calculate_frame_start(mock_animation):
    """At 0ms, should be at index 0."""
    result = SimulatorService.calculate_frame(mock_animation, 0)
    assert result.frame_index == 0
    assert result.frame_progress == 0.0


def test_calculate_frame_mid(mock_animation):
    """At 50ms, should be halfway through first frame (index 0)."""
    result = SimulatorService.calculate_frame(mock_animation, 50)
    assert result.frame_index == 0
    assert result.frame_progress == 0.5


def test_calculate_frame_transition(mock_animation):
    """At 150ms, should be halfway through second frame (index 1)."""
    result = SimulatorService.calculate_frame(mock_animation, 150)
    assert result.frame_index == 1
    assert result.frame_progress == 0.5


def test_calculate_frame_loop(mock_animation):
    """Animation duration is 200ms. At 250ms, should wrap to 50ms (index 0)."""
    result = SimulatorService.calculate_frame(mock_animation, 250)
    assert result.frame_index == 0
    assert result.frame_progress == 0.5


def test_calculate_no_loop(mock_animation):
    """With loop=False, should stop at last frame if elapsed > duration."""
    config = SimulationConfig(loop=False)
    result = SimulatorService.calculate_frame(mock_animation, 300, config)
    assert result.frame_index == 1  # Last frame index
    assert result.is_finished is True


def test_empty_animation():
    anim = Animation(name="Empty", frames=[])
    result = SimulatorService.calculate_frame(anim, 100)
    assert result.frame_index == 0
    assert result.is_finished is True
