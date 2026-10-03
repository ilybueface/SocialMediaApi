import asyncio
import os
import logging
from aiogram import Bot
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

load_dotenv()


class TelegramLogHandler(logging.Handler):
    def __init__(self, chat_id):
        super().__init__()
        tg_token = os.getenv("TELEGRAMM_KEY")
        self.chat_id = chat_id
        self.bot = Bot(
            token=tg_token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
        )

    def emit(self, record):
        message = self.format(record)
        asyncio.run(self.bot.send_message(chat_id=self.chat_id, text=message))
