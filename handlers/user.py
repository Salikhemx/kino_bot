from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.exceptions import TelegramBadRequest

from database import get_movie, get_channel

router = Router()


async def is_subscribed(bot, user_id):
    channel = get_channel()

    if not channel:
        return True

    try:
        member = await bot.get_chat_member(channel, user_id)
        return member.status in ("creator", "administrator", "member")
    except TelegramBadRequest:
        return False


@router.message(F.text & ~F.text.startswith("/"))
async def movie_handler(message: Message):

    channel = get_channel()

    if channel:
        ok = await is_subscribed(message.bot, message.from_user.id)

        if not ok:
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="📢 Kanalga obuna bo'lish",
                            url=f"https://t.me/{channel.replace('@','')}"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="✅ Tekshirish",
                            callback_data="check_sub"
                        )
                    ]
                ]
            )

            await message.answer(
                "❌ Avval kanalga obuna bo'ling.",
                reply_markup=keyboard
            )
            return

    code = message.text.strip()

    movie = get_movie(code)

    if movie:
        await message.answer_video(movie)
    else:
        await message.answer("❌ Bunday kodli kino topilmadi.")

        from aiogram.types import CallbackQuery


@router.callback_query(F.data == "check_sub")
async def check_subscribe(callback: CallbackQuery):

    channel = get_channel()

    if not channel:
        await callback.answer("Kanal topilmadi.", show_alert=True)
        return

    ok = await is_subscribed(
        callback.bot,
        callback.from_user.id
    )

    if ok:
        await callback.message.edit_text(
            "✅ Rahmat! Endi kino kodini yuboring."
        )
    else:
        await callback.answer(
            "❌ Siz hali obuna bo'lmagansiz.",
            show_alert=True
        )