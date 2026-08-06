import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN

from handlers.start import router as start_router
from handlers.user import router as user_router
from handlers.admin import router as admin_router
from handlers.panel import router as panel_router


async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    dp = Dispatcher()

    # Routerlar
    dp.include_router(admin_router)
    dp.include_router(panel_router)
    dp.include_router(start_router)
    dp.include_router(user_router)

    print("✅ Bot ishga tushdi!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())