import asyncio
from app.handlers import router
from aiogram import Bot, Dispatcher

async def main():
    bot = Bot(token='______')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('BOT OFF')
