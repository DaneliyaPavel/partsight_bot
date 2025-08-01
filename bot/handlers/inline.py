from __future__ import annotations

from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import settings

router = Router()


def get_main_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Формирует главное меню.
      • Для всех — «Загрузить DOCX», «О боте».
      • Для админов (+)  «Обновить каталог».
    """
    rows: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text="📄 Загрузить DOCX",
                callback_data="upload_file",
            )
        ],
        [
            InlineKeyboardButton(
                text="ℹ️ О боте",
                callback_data="about_bot",
            )
        ],
    ]

    # кнопка только админу
    if user_id in settings.ADMINS:
        rows.append(
            [
                InlineKeyboardButton(
                    text="🔄 Обновить каталог",
                    callback_data="upload_cat",
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=rows)
