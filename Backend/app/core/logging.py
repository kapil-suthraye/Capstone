import sys

from loguru import logger

from Backend.app.core.config import settings

logger.remove()

logger.add(
    sys.stdout,
    level=settings.LOG_LEVEL,
    colorize=not settings.LOG_JSON,
    enqueue=True,
    serialize=settings.LOG_JSON,
    backtrace=False,
    diagnose=False,
)


def bind_logger(**kwargs):
    return logger.bind(**kwargs)