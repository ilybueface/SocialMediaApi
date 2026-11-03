import asyncio
import html
import os
import logging
import threading
from aiogram import Bot
from dotenv import load_dotenv
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

load_dotenv()


class TelegramLogHandler(logging.Handler):
    def __init__(self, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = Bot(
            token=os.getenv("TELEGRAMM_KEY"),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

    def emit(self, record):
        message = self.format(record)
        safe_message = html.escape(message)
        truncated_message = safe_message[-4096:]
        def run_async():
            asyncio.run(
                self.bot.send_message(chat_id=self.chat_id, text=truncated_message)
            )

        threading.Thread(target=run_async, daemon=True).start()
