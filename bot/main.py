import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties

from bot.config import settings
from bot.handlers import register_all_handlers
from bot.service.loader import load_catalog
from bot.utils.logger import setup as setup_logging
from loguru import logger


async def main() -> None:
    setup_logging()

    await load_catalog()

    bot = Bot(
        token=settings.BOT_TOKEN,
        proxy=settings.PROXY_URL,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await bot.delete_webhook(drop_pending_updates=True)

    dp = Dispatcher()
    register_all_handlers(dp)

    logger.info("🤖  Bot started (polling)")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
