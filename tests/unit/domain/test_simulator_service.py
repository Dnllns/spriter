import uuid
from src.domain.simulator import SimulatorService, SimulationConfig
from src.domain.entities import Animation, Frame


class TestSimulatorService:
    def test_calculate_frame_empty_animation(self):
        """Should handle empty animations gracefully"""
        anim = Animation(id=str(uuid.uuid4()), name="Empty", frames=[], loop=True)
        result = SimulatorService.calculate_frame(anim, 1000)
        assert result.frame_index == 0
        assert result.is_finished is True

    def test_calculate_frame_basic_loop(self):
        """Should calculate correct frame for looping animation"""
        frames = [
            Frame(id=str(uuid.uuid4()), duration_ms=100, index=0),
            Frame(id=str(uuid.uuid4()), duration_ms=100, index=1),
        ]
        anim = Animation(id=str(uuid.uuid4()), name="Loop", frames=frames, loop=True)

        # At 50ms -> Frame 0
        result = SimulatorService.calculate_frame(anim, 50)
        assert result.frame_index == 0

        # At 150ms -> Frame 1
        result = SimulatorService.calculate_frame(anim, 150)
        assert result.frame_index == 1

        # At 250ms -> Frame 0 (Back to start)
        result = SimulatorService.calculate_frame(anim, 250)
        assert result.frame_index == 0

    def test_calculate_frame_no_loop_finished(self):
        """Should stop at last frame if loop=False"""
        frames = [
            Frame(id=str(uuid.uuid4()), duration_ms=100, index=0),
            Frame(id=str(uuid.uuid4()), duration_ms=100, index=1),
        ]
        anim = Animation(
            id=str(uuid.uuid4()), name="OneShot", frames=frames, loop=False
        )  # Fix loop usage via config override if needed
        config = SimulationConfig(loop=False)

        # At 250ms -> Frame 1 (Last frame), finished
        result = SimulatorService.calculate_frame(anim, 250, config=config)
        assert result.frame_index == 1
        assert result.is_finished is True

    def test_calculate_frame_playback_speed(self):
        """Should account for playback speed"""
        frames = [
            Frame(id=str(uuid.uuid4()), duration_ms=100, index=0),
            Frame(id=str(uuid.uuid4()), duration_ms=100, index=1),
        ]
        anim = Animation(id=str(uuid.uuid4()), name="Speedy", frames=frames, loop=True)
        config = SimulationConfig(playback_speed=2.0, loop=True)

        # At 26ms * 2.0 = 52ms -> Frame 0
        result = SimulatorService.calculate_frame(anim, 26, config=config)
        assert result.frame_index == 0

        # At 75ms * 2.0 = 150ms -> Frame 1
        result = SimulatorService.calculate_frame(anim, 75, config=config)
        assert result.frame_index == 1

    def test_calculate_frame_zero_duration(self):
        """Should handle frames with zero duration"""
        frames = [Frame(id=str(uuid.uuid4()), duration_ms=0, index=0)]
        anim = Animation(id=str(uuid.uuid4()), name="Instant", frames=frames)
        result = SimulatorService.calculate_frame(anim, 100)
        assert result.is_finished is True
