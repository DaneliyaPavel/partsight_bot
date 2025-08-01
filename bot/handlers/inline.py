from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router

router = Router()


def get_main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📄 Загрузить файл DOCX", callback_data="upload_file"
                )
            ],
            [InlineKeyboardButton(text="ℹ️ О боте", callback_data="about_bot")],
        ]
    )
