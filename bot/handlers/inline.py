"""
Inline-keyboard helpers, формируют клавиатуры для разных сценариев.
"""

from __future__ import annotations
from aiogram import Router

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.config import settings
from bot.service import last_act

router = Router()


def get_main_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Главное меню.

    ▸ «📄 Загрузить DOCX»          — всегда
    ▸ «🔄 Последний акт»           — если есть кешированный file_id
    ▸ «📂 Обновить каталог»        — только для админов
    ▸ «ℹ️ О боте»                  — всегда
    """
    buttons: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text="📄 Загрузить DOCX",
                callback_data="upload_file",
            )
        ]
    ]

    # «Повторить последний акт»
    if last_act.exists(user_id):
        buttons.append(
            [
                InlineKeyboardButton(
                    text="🔄 Последний акт",
                    callback_data="repeat_last",
                )
            ]
        )

    # «Обновить каталог» (только админы)
    if user_id in settings.ADMINS:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="📂 Обновить каталог",
                    callback_data="upload_cat",
                )
            ]
        )

    # «О боте» — всегда внизу
    buttons.append(
        [
            InlineKeyboardButton(
                text="ℹ️ О боте",
                callback_data="about_bot",
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)
