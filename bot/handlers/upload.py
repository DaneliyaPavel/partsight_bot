import os
from pathlib import Path

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from loguru import logger

from bot.service.generator import build_act
from bot.service.parser import parse_request_docx
from bot.service.loader import load_catalog
from bot.service.matcher import can_produce

router = Router()
DOCX = (
    F.document.mime_type
    == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)


async def _process_docx(tmp_in: Path) -> Path:
    rows = parse_request_docx(tmp_in)
    catalog_pref = await load_catalog()

    packs = []
    for row in rows:
        ok = can_produce(row["naimenovanie"], catalog_pref)
        packs.append(
            {
                "material": row["material"],
                "naimenovanie": row["naimenovanie"],
                "vozmoznost": "да" if ok else "нет",
                "rekomendacii": (
                    "Производство возможно при предоставлении оригинального изделия "
                    "или чертежа завода-изготовителя"
                    if ok
                    else "Производство не возможно"
                ),
            }
        )

    return build_act(packs)


@router.message(DOCX)
async def handle_any_docx(message: Message, state: FSMContext) -> None:
    tmp_in: Path = Path("/tmp") / message.document.file_name
    file = await message.bot.download(message.document)
    tmp_in.write_bytes(file.read())
    logger.info("Получен DOCX от %s: %s", message.from_user.id, tmp_in.name)

    try:
        act_path = await _process_docx(tmp_in)
        logger.info("Сформирован акт: %s", act_path.name)

        await message.answer_document(
            document=FSInputFile(act_path),
            caption="✅ Готово! Акт сформирован.",
        )
    except Exception as err:
        logger.exception("Ошибка при формировании акта")
        await message.answer(f"❌ Ошибка: {err}")
    finally:
        try:
            os.remove(tmp_in)
        except OSError:
            pass
        await state.clear()
