from __future__ import annotations

import contextlib
import logging
from pathlib import Path

from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.types import FSInputFile, Message

from bot.service.generator import build_act
from bot.service.loader import load_catalog
from bot.service.matcher import can_produce
from bot.service.parser import parse_request_docx
from bot.service import last_act
from bot.handlers.inline import get_main_keyboard

router = Router()
log = logging.getLogger(__name__)

TMP_DIR = Path("/tmp")


async def _process_docx(src: Path) -> Path:
    rows = parse_request_docx(src)
    pref = await load_catalog()

    packs = []
    for r in rows:
        possible = "да" if can_produce(r["naimenovanie"], pref) else "нет"
        rekom = (
            "Производство возможно при предоставлении оригинального изделия или чертежа завода-изготовителя"
            if possible == "да"
            else "Производство не возможно"
        )
        packs.append(
            {
                "material": r["material"],
                "naimenovanie": r["naimenovanie"],
                "vozmoznost": possible,
                "rekomendacii": rekom,
            }
        )

    return build_act(packs)


@router.message(F.document.file_name.endswith(".docx"))
async def handle_any_docx(
    message: Message,
) -> None:  # noqa: C901 — удобнее читать целиком
    user_id = message.from_user.id
    doc = message.document
    tmp_in = TMP_DIR / doc.file_name

    # 1️⃣ первая «ступень» прогресса
    progress: Message = await message.answer("📥 Файл получен, готовлюсь к обработке…")

    try:
        # chat action + загрузка
        await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        await message.bot.download(doc, destination=tmp_in)
        log.info("Получен DOCX от %s: %s", user_id, doc.file_name)

        # 2️⃣ вторая ступень
        await progress.edit_text("⏳ Анализирую документы и формирую акт…")

        act_path = await _process_docx(tmp_in)

        # 3️⃣ отправляем акт
        await message.bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_DOCUMENT)
        sent = await message.answer_document(
            document=FSInputFile(act_path),
            caption="✅ Акт готов!",
        )

        # 4️⃣ кэшируем file_id
        last_act.set_(user_id, sent.document.file_id)
        log.info("Сформирован акт: %s (file_id cached)", act_path)

        # 5️⃣ показываем кнопки и удаляем «прогресс»
        await progress.delete()
        await message.answer(
            "Можете повторно получить этот акт:",
            reply_markup=get_main_keyboard(user_id),
        )

    except Exception as exc:  # noqa: BLE001
        log.exception("Ошибка при формировании акта")
        await progress.edit_text(f"❌ Ошибка: {exc.__class__.__name__}")
    finally:
        with contextlib.suppress(Exception):
            tmp_in.unlink(missing_ok=True)
