import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from handlers.bot import BotHandler
from handlers.filter import FilterHandler
from handlers.user import UserHandler
from loader import bot, dp
from tools.web_scrapping import WebScrapping

class TelegramBot(BotHandler, FilterHandler, UserHandler):
    def __init__(self):
        pass

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

async def main():
    telegram_bot = TelegramBot()
    await telegram_bot.start()

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            logging.error(f"Bot crashed with error: {e}")
            logging.info("Restarting bot in 5 seconds...")
            asyncio.sleep(5)  # Wait for 5 seconds before restarting
