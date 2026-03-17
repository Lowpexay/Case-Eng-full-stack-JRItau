import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.database import Base, engine
from app.routers import auth_router, game_router, ranking_router, user_router
from app.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)


def configure_app_logging() -> None:
    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.INFO)
    if not app_logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
        )
        app_logger.addHandler(handler)
    app_logger.propagate = False


configure_app_logging()

# Create tables on startup (for SQLite / dev convenience)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mastermind API",
    description="API para o jogo Mastermind — desafio técnico Full-Stack Jr.",
    version="1.0.0",
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Exception handlers ────────────────────────────────────────────────────────
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router.router)
app.include_router(game_router.router)
app.include_router(ranking_router.router)
app.include_router(user_router.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Mastermind API está no ar!"}
