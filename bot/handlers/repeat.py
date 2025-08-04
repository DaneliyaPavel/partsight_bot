# bot/handlers/repeat.py
from aiogram import F, Router, Bot
from aiogram.enums import ChatAction
from aiogram.types import CallbackQuery

from bot.service import last_act

router = Router()


@router.callback_query(F.data == "repeat_last")
async def repeat_last(cb: CallbackQuery, bot: Bot) -> None:
    """
    Шлём сохранённый (cached) file_id последнего акта.
    Кнопка видна только если он есть – см. inline.get_main_keyboard().
    """
    user_id = cb.from_user.id
    file_id = last_act.get(user_id)

    if not file_id:
        await cb.answer("Нет сохранённого акта.", show_alert=True)
        return

    await cb.answer()  # закрываем «часики» на кнопке
    await bot.send_chat_action(cb.message.chat.id, ChatAction.UPLOAD_DOCUMENT)
    await bot.send_document(
        chat_id=cb.message.chat.id,
        document=file_id,
        caption="🔄 Ваш последний акт",
    )
