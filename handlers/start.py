from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

router = Router()

@router.message(CommandStart())
async def start(message: Message):

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎬 Kanal",
                    url="https://t.me/kinolar12026"
                )
            ],
            [
                InlineKeyboardButton(
                    text="👨‍💻 Admin",
                    url="https://t.me/Kino_Go2026_bot"
                )
            ]
        ]
    )

    await message.answer(
        """
🎬 <b>Kino Go botiga xush kelibsiz!</b>

🎥 Eng yangi HD kinolar
🍿 Seriallar
🎞 Multfilmlar

📥 Kino kodini yuboring va kinoni darhol oling.

⭐ Sizga maroqli tomosha tilaymiz!
        """,
        reply_markup=keyboard
    )