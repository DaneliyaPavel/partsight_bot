# bot/main.py
from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties  # ← добавили
from aiohttp import web

from bot.config import settings
from bot.handlers import register_all_handlers
from bot.health import create_app


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s — %(message)s",
        datefmt="%H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    logging.getLogger("aiohttp.access").setLevel(logging.WARNING)


async def main() -> None:
    _setup_logging()

    bot = Bot(
        token=settings.BOT_TOKEN,
        proxy=settings.PROXY_URL,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),  # ← фикс
    )

    dp = Dispatcher(storage=MemoryStorage())
    register_all_handlers(dp)

    app = create_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=8080)
    await site.start()

    logging.getLogger(__name__).info("🤖  Bot started (polling)")
    await dp.start_polling(bot)


if __name__ == "__main__":
    Path("output").mkdir(exist_ok=True)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
