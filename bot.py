import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import  Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.db.models import async_main
from config import TOKEN
from app.handlers import router
import app.keyboards as kb


async def main():
    await async_main()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
