from __future__ import annotations

from pathlib import Path

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from loguru import logger

from bot.config import settings
from bot.service.loader import load_catalog

router = Router()

CAT_PATH = settings.CATALOG_PATH


# ───────────────────── кнопка «🔄 Обновить каталог» ─────────────────────
@router.callback_query(F.data == "upload_cat")
async def ask_cat(callback: CallbackQuery) -> None:
    if callback.from_user.id not in settings.ADMINS:
        await callback.answer("⛔️ Только админ.")
        return

    await callback.message.answer(
        "Пришлите новый файл каталога (*.xlsb). Старый будет заменён."
    )
    await callback.answer()


# ───────────────────── приём любого документа ──────────────────────────
@router.message(F.document)
async def handle_catalog_file(msg: Message) -> None:
    if msg.from_user.id not in settings.ADMINS:
        return

    doc = msg.document
    if not doc.file_name.lower().endswith(".xlsb"):
        await msg.answer("⚠️ Нужен файл с расширением .xlsb")
        return

    # сохраняем во временный файл
    tmp = Path("/tmp") / doc.file_name
    file_obj = await msg.bot.download(doc)
    tmp.write_bytes(file_obj.read())

    # заменяем каталог
    CAT_PATH.parent.mkdir(exist_ok=True)
    tmp.replace(CAT_PATH)
    logger.info("Каталог обновлён админом {}", msg.from_user.id)

    # перечитываем кеш и считаем префиксы
    pref_set = await load_catalog(force=True)
    await msg.answer(
        f"✅ Каталог обновлён, префиксов: <b>{len(pref_set):,}</b>", parse_mode="HTML"
    )
