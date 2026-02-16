from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..domain.entities import Animation
from ..domain.simulator import FrameResult, SimulationConfig, SimulatorService

router = APIRouter(tags=["simulator"])


class SimulateRequest(BaseModel):
    animation: Animation
    elapsed_ms: int
    config: SimulationConfig | None = None


@router.post("/simulate", response_model=FrameResult)
async def simulate_frame(request: SimulateRequest):
    """
    Calculates the current frame for a given animation and elapsed time.
    """
    if request.elapsed_ms < 0:
        # Pydantic might catch this if we use Field(ge=0),
        # but for AC-004-02 we can also check here.
        raise HTTPException(status_code=422, detail="elapsed_ms must be non-negative")

    return SimulatorService.calculate_frame(
        request.animation, request.elapsed_ms, request.config
    )
