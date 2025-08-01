from pathlib import Path
from loguru import logger

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def setup() -> None:
    # файл + цветной stdout
    logger.remove()
    logger.add(
        LOG_DIR / "bot.log",
        rotation="10 MB",
        retention="10 days",
        compression="zip",
        level="INFO",
        enqueue=True,
        backtrace=False,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name}:{function}:{line} — {message}",
    )
    logger.add(
        sink=lambda msg: print(msg, end=""),
        colorize=True,
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>{name}</cyan> — <level>{message}</level>",
    )
