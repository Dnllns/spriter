from pydantic import BaseModel

from src.domain.entities import Animation


class SimulationConfig(BaseModel):
    playback_speed: float = 1.0  # Multiplier (e.g., 0.5x, 2.0x)
    loop: bool = True
    reverse: bool = False


class FrameResult(BaseModel):
    frame_index: int
    frame_progress: float  # 0.0 to 1.0 within the frame
    is_finished: bool = False


class SimulatorService:
    """Core logic for sprite animation simulation."""

    @staticmethod
    def calculate_frame(
        animation: Animation, elapsed_ms: int, config: SimulationConfig | None = None
    ) -> FrameResult:
        """
        Calculates the current frame based on elapsed time and configuration.
        """
        if not animation.frames:
            return FrameResult(frame_index=0, frame_progress=0.0, is_finished=True)

        config = config or SimulationConfig(loop=animation.loop)

        # Calculate total duration of one loop
        total_duration = sum(f.duration_ms for f in animation.frames)
        if total_duration == 0:
            return FrameResult(frame_index=0, frame_progress=0.0, is_finished=True)

        # Apply playback speed
        adjusted_elapsed = elapsed_ms * config.playback_speed

        # Handle looping
        if config.loop:
            current_time = adjusted_elapsed % total_duration
            is_finished = False
        else:
            if adjusted_elapsed >= total_duration:
                # animation finished, return last frame
                last_idx = len(animation.frames) - 1
                return FrameResult(
                    frame_index=last_idx, frame_progress=1.0, is_finished=True
                )
            current_time = adjusted_elapsed
            is_finished = False

        # Find the frame corresponding to current_time
        accumulated_time = 0
        for i, frame in enumerate(animation.frames):
            frame_duration = frame.duration_ms
            if accumulated_time + frame_duration > current_time:
                # We are in this frame
                time_in_frame = current_time - accumulated_time
                progress = time_in_frame / frame_duration
                return FrameResult(
                    frame_index=i, frame_progress=progress, is_finished=is_finished
                )
            accumulated_time += frame_duration

        # Fallback (should not happen due to modulo logic, but for safety)
        return FrameResult(
            frame_index=len(animation.frames) - 1, frame_progress=1.0, is_finished=True
        )
