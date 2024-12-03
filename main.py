import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import TOKEN
from db.engine import sessionmarker, create_db
from db.orm_query import create_question, create_answer
from middlewaris.db import DBMiddleware
from aiogram.enums import ParseMode

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(msg: Message):
    await msg.answer(text="Привет, какой у вас вопрос?")


@dp.message((F.text) & (F.chat.id != 1526741555))
async def question(msg: Message, session: AsyncSession):
    await create_question(msg.chat.id, msg.text, session)
    await bot.send_message(chat_id=1526741555, text=msg.text)
    await msg.answer("<i>Вопрос отправлен</i>", parse_mode=ParseMode.HTML)


@dp.message((F.reply_to_message) & (F.chat.id == 1526741555))
async def answer(msg: Message, session):
    chat_id = await create_answer(msg.reply_to_message.text, session)
    await bot.send_message(chat_id=chat_id, text=f"<b>Ответ от техподдержки\n</b> {msg.text}", parse_mode=ParseMode.HTML)
    await msg.answer(text="<i>Ответ отправлен</i>", parse_mode=ParseMode.HTML)


async def startup():
     await create_db()


async def main():

    dp.startup.register(startup)
    dp.update.middleware(DBMiddleware(sessionmarker=sessionmarker))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())