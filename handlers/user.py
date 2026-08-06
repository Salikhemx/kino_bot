from aiogram import Router, F
from aiogram.types import Message

from database import get_movie

router = Router()


@router.message(F.text & ~F.text.startswith("/"))
async def movie_handler(message: Message):
    code = message.text.strip()

    movie = get_movie(code)

    if movie:
        await message.answer_video(movie)
    else:
        await message.answer("❌ Bunday kodli kino topilmadi.")