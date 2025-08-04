# bot/handlers/start.py
from __future__ import annotations

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from .inline import get_main_keyboard
from bot.service.form import FormStates

router = Router()


# ───────────────────────── /start ─────────────────────────
@router.message(CommandStart())
async def cmd_start(msg: Message, state: FSMContext) -> None:
    await state.clear()
    await msg.answer(
        "👋 Привет! Я бот, который помогает проверять перечни ЗИП и формировать акты.\n\n"
        "Выберите действие:",
        reply_markup=get_main_keyboard(msg.from_user.id),
    )


# ─────────────────────── «О боте» ────────────────────────
@router.callback_query(F.data == "about_bot")
async def about_bot(cb: CallbackQuery) -> None:
    await cb.message.answer(
        "📌 <b>О боте</b>\n\n"
        "Загрузите .docx с перечнем ЗИП — я сопоставлю позиции с каталогом "
        "произведённой продукции и отправлю готовый акт.",
        parse_mode="HTML",
    )


# ─────────────────── «Загрузить файл» ────────────────────
@router.callback_query(F.data == "upload_file")
async def ask_file(cb: CallbackQuery, state: FSMContext) -> None:
    await cb.message.answer(
        "📄 Пожалуйста, отправьте .docx-файл с перечнем ЗИП для анализа."
    )
    await state.set_state(FormStates.waiting_for_file)
