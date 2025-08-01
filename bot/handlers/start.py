from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Message,
    CallbackQuery,
)

from bot.service.form import FormStates

router = Router()

keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📝 Сгенерировать акт", callback_data="upload_file"
            )
        ],
        [InlineKeyboardButton(text="ℹ️ О боте", callback_data="about_bot")],
    ]
)


@router.message(CommandStart())
async def cmd_start(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer(
        "Здравствуйте! Этот бот поможет вам:\n\n"
        "— Проверить позиции из перечня ЗИП\n"
        "— Сопоставить их с уже произведёнными изделиями\n"
        "— Сформировать акт по результатам проверки\n\n"
        "Выберите действие ниже:",
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "about_bot")
async def about_bot(cb: CallbackQuery) -> None:
    await cb.message.answer(
        "📌 *О боте*\n\n"
        "Этот бот предназначен для обработки перечней ЗИП, полученных от комиссии по параллельному импорту. "
        "Он сопоставляет указанные позиции с каталогом уже произведённой продукции и формирует акт с результатами.\n\n"
        "Формат поддерживаемых файлов: `.docx`.\n"
        "Для начала загрузите файл с перечнем позиций."
    )


@router.callback_query(F.data == "upload_file")
async def ask_file(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.answer(
        "📄 Пожалуйста, отправьте .docx файл с перечнем ЗИП для анализа."
    )
    await state.set_state(FormStates.waiting_for_file)
