import asyncio
from app.handlers import router
from aiogram import Bot, Dispatcher

async def main():
    bot = Bot(token='7862382488:AAGR3hEZO8YFl-95NiV7pxLvQyO2_1J5qR8')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('BOT OFF')