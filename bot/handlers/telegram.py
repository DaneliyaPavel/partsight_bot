from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Set

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from loguru import logger

from bot.config import settings
from bot.catalog.loader import load_catalog
from bot.word.parser import parse_request_docx
from bot.word.generator import build_act
from bot.service.matcher import can_produce

# --- Telegram bot init -------------------------------------------------
bot = Bot(token=settings.BOT_TOKEN, proxy=settings.PROXY_URL)
dp = Dispatcher()

CATALOG_PREF: Set[str]  # заполним при старте


@dp.message(F.text == "/start")
async def cmd_start(m: Message) -> None:
    await m.answer("👋 Пришлите DOCX-запрос — отправлю акт с оценкой.")


def _process_request(file_path: Path) -> Path:
    items = parse_request_docx(file_path)
    packets = []
    for it in items:
        ok = can_produce(it["naimenovanie"], CATALOG_PREF)
        packets.append(
            dict(
                material=it["material"],
                naimenovanie=it["naimenovanie"],
                vozmoznost="да" if ok else "нет",
                rekomendacii=(
                    "Производство возможно."
                    if ok
                    else "На данный момент производство отсутствует."
                ),
            )
        )
    return build_act(packets)


@dp.message(F.document)
async def doc_handler(m: Message) -> None:
    doc = m.document
    in_path = Path("incoming") / doc.file_name
    in_path.parent.mkdir(exist_ok=True)

    await bot.download(doc, destination=in_path)
    await m.reply(f"Файл «{in_path.name}» получен, обрабатываю…")

    act_path = await asyncio.to_thread(_process_request, in_path)
    await m.reply_document(FSInputFile(act_path), caption="Готовый акт ✅")


async def _run() -> None:
    global CATALOG_PREF
    CATALOG_PREF = await load_catalog()
    logger.info("Каталог загружен, префиксов: {}", len(CATALOG_PREF))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


def run_bot() -> None:
    logger.add("logs/bot_{time}.log", rotation="10 MB", compression="zip")
    asyncio.run(_run())
