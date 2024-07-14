from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

from database.managers import FilterManager, UserManager
from keyboards.default.markups import get_reply_markup
from loader import BOT_KEY, bot, dp, storage

from .filter import PriceFilter


class BotHandler:
    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):
        start_text = "Salam, mən Botam🤖. turbo.az-da ən son qoyulan avtomobilləri filter ilə sənə bildirim göndərə bilərəm🚗."
        await message.answer(start_text, parse_mode="Markdown")

        UserManager().get_or_create(
            tg_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            full_name=message.from_user.full_name,
        )

        FilterManager().get_or_create(tg_id=message.from_user.id)

        maksimum_price_text = "Gözləyin...⌛️"

        await message.answer(
            maksimum_price_text,
            parse_mode="Markdown",
        )

    @dp.message_handler(commands=["help"])
    async def help(message: types.Message):
        await message.answer("I can't help you. I'm just a bot.")
