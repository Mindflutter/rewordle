import uvicorn
from fastapi import FastAPI

from db.database import db
from metrics import metrics_instrumentator
from routes import main_router
from settings import LOGGING_CONFIG, settings


def get_app():
    _app = FastAPI(
        title="Rewordle",
        version="0.0.1",
        description="A famous word game reloaded",
    )

    _app.include_router(main_router)
    metrics_instrumentator.instrument(_app).expose(_app, tags=["service"])

    @_app.on_event("startup")
    async def startup():
        await db.init()

    @_app.on_event("shutdown")
    async def shutdown():
        await db.close()

    return _app


def main():
    uvicorn.run(
        app="asgi:app",
        workers=settings.WORKERS,
        reload=settings.RELOAD,
        host=settings.HOST,
        port=settings.PORT,
        log_config=LOGGING_CONFIG,
        access_log=True,
    )


if __name__ == "__main__":
    main()
