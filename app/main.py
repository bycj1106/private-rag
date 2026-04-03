from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import ensure_data_dirs, get_settings
from app.api.routes import router
from app.db.sqlite import init_db


def init_runtime() -> None:
    ensure_data_dirs()
    init_db()


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_runtime()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Private RAG Knowledge Base",
        description="Personal RAG Knowledge Base API for AI application development learning",
        version="1.0.0",
        lifespan=lifespan,
    )

    settings = get_settings()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    app.include_router(router, prefix="/api")
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
