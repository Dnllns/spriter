from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}
