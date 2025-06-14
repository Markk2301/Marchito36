from aiogram import Dispatcher, Bot
import asyncio
from config import TOKEN
from handlers.commands import command_router

dp = Dispatcher()
dp.include_router(command_router)

async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())