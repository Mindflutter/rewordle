from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False
    WORKERS: int = 1
    LOG_LEVEL: str = "INFO"
    DB_DSN: str = "postgresql+asyncpg://rewordle:rewordle@localhost:5432/rewordle"
    MIGRATION_DSN: str = "postgresql+psycopg2://rewordle:rewordle@localhost:5432/rewordle"
    DB_CONN_TRIES: int = 5


settings = Settings()

PROJECT_ROOT = Path(__file__).parents[1]
DICTIONARY_PATH = PROJECT_ROOT / "src/resources/dictionary.txt"
# load dictionary
with open(DICTIONARY_PATH) as dict_file:
    WORDS = dict_file.read().splitlines()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "service": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": settings.LOG_LEVEL,
            "formatter": "service",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {"handlers": ["default"], "level": settings.LOG_LEVEL, "propagate": False},
        "sqlalchemy": {"handlers": ["default"], "level": "WARNING", "propagate": False},
    },
}
