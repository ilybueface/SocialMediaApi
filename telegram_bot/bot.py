import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message, TelegramObject, User
from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = os.getenv("TELEGRAMM_KEY")
ADMIN_ID = int(os.getenv("TELEGRAMM_CHAT_ID"))

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

dp = Dispatcher()


class AdminOnlyMiddleWare(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        user: User = data.get("event_from_user")

        if not user or user.id != ADMIN_ID:
            return
        return await handler(event, data)


@dp.message(Command("start"))
async def start_message(
    message: Message,
):
    user_name = message.from_user.first_name
    user_lang = message.from_user.language_code

    if user_lang == "ru":
        text = f"Привет, {user_name}! Рад тебя видеть."
    else:
        text = f"Hello, {user_name}! Glad to see you."

    await message.answer(text)


@dp.message(Command("help"))
async def help_message(
    message: Message,
):
    text = (
        "❓ *Справка по боту*\n\n"
        "/start — Перезапустить бота\n"
        "/profile — Посмотреть личный кабинет\n"
    )

    await message.answer(text, parse_mode=ParseMode.MARKDOWN)


async def main():
    dp.message.outer_middleware(AdminOnlyMiddleWare())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
