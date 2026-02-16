from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .domain.exceptions import SpriteNotFoundError, UnauthorizedError
from .presentation.routers import router as sprite_router
from .presentation.simulator_router import router as simulator_router

app = FastAPI(
    title="Spriter API",
    description="Advanced Sprite Repository & Simulator",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
origins = ["*"]  # For development, tighten in production

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sprite_router, prefix="/api/v1")
app.include_router(simulator_router, prefix="/api/v1")


@app.exception_handler(SpriteNotFoundError)
async def sprite_not_found_exception_handler(
    request: Request, exc: SpriteNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(UnauthorizedError)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedError):
    return JSONResponse(
        status_code=403,
        content={"detail": str(exc)},
    )


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}
