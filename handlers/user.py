from aiogram import types

from database.managers import UserManager
from loader import bot, dp


class UserHandler:
    @dp.message_handler(commands=["bildirim"])
    async def set_notification(message: types.Message):
        user = UserManager().get_user(tg_id=message.from_user.id)
        notification = not user.notification
        UserManager().update_user(tg_id=message.from_user.id, notification=notification)

        text = "Açılıdı🔑" if notification else "Bağlalandı🔐"
        await message.answer(
            f"Bildirim *{text}*",
            parse_mode="Markdown",
        )
