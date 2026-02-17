import time
import uuid

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .domain.exceptions import SpriteNotFoundError, UnauthorizedError
from .logging_config import setup_logging
from .presentation.routers import router as sprite_router
from .presentation.simulator_router import router as simulator_router

setup_logging()
logger = structlog.get_logger()

app = FastAPI(
    title="Spriter API",
    description="Advanced Sprite Repository & Simulator",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Mount Static Files
try:
    app.mount("/static", StaticFiles(directory="src/static"), name="static")
except RuntimeError:
    # Fallback for when running tests or different cwd
    import os

    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
        name="static",
    )

# Templates
try:
    templates = Jinja2Templates(directory="src/templates")
except Exception:
    import os

    templates = Jinja2Templates(
        directory=os.path.join(os.path.dirname(__file__), "templates")
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


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)

    start_time = time.perf_counter()

    try:
        response = await call_next(request)
    except Exception as e:
        logger.exception("unhandled_exception", error=str(e))
        response = JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"},
        )

    process_time = time.perf_counter() - start_time
    status_code = response.status_code
    logger.info(
        "http_request",
        method=request.method,
        path=request.url.path,
        status=status_code,
        duration=f"{process_time:.4f}s",
    )

    response.headers["X-Request-ID"] = request_id
    return response


app.include_router(sprite_router, prefix="/api/v1")
app.include_router(simulator_router, prefix="/api/v1")


@app.get("/", include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.exception_handler(SpriteNotFoundError)
async def sprite_not_found_exception_handler(
    request: Request, exc: SpriteNotFoundError
):
    logger.warning("sprite_not_found", error=str(exc))
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(UnauthorizedError)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedError):
    logger.warning("unauthorized_access", error=str(exc))
    return JSONResponse(
        status_code=403,
        content={"detail": str(exc)},
    )


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}
