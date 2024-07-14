import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from handlers.bot import BotHandler
from handlers.filter import FilterHandler
from handlers.user import UserHandler
from loader import bot, dp
from tools.web_scrapping import WebScrapping


class TelegramBot(BotHandler, FilterHandler, UserHandler):
    def __init__(self):
        self.loop = asyncio.new_event_loop()

    async def start_bot(self):
        while True:
            try:
                await dp.start_polling()
            except Exception as e:
                logging.error(e)
                await asyncio.sleep(5)

    async def start_scrapper(self):
        await WebScrapping().start()

    async def start(self):
        await asyncio.gather(self.start_bot(), self.start_scrapper())


if __name__ == "__main__":
    telegram_bot = TelegramBot()
    telegram_bot.loop.run_until_complete(telegram_bot.start())
