from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.enums import ChatMemberStatus

from database import (
    get_movie,
    get_channel,
    add_user
)

router = Router()


async def check_sub(bot, user_id):
    channel = get_channel()

    if not channel:
        return True

    try:
        member = await bot.get_chat_member(channel, user_id)

        return member.status in (
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR,
        )

    except Exception:
        return False


@router.message(F.text)
async def movie_handler(message: Message):

    if message.text.startswith("/"):
        return

    # Foydalanuvchini bazaga saqlash
    add_user(message.from_user.id)

    channel = get_channel()

    if channel:

        ok = await check_sub(
            message.bot,
            message.from_user.id
        )

        if not ok:

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="📢 Kanalga obuna bo'lish",
                            url=f"https://t.me/{channel.replace('@', '')}"
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
                "❌ Avval kanalga obuna bo'ling!",
                reply_markup=keyboard
            )

            return

    movie = get_movie(message.text.strip())

    if movie:
        await message.answer_video(movie)
    else:
        await message.answer(
            "❌ Bunday kodli kino topilmadi."
        )


@router.callback_query(F.data == "check_sub")
async def check_button(callback: CallbackQuery):

    ok = await check_sub(
        callback.bot,
        callback.from_user.id
    )

    if ok:

        await callback.message.edit_text(
            "✅ Obuna tasdiqlandi!\n\n🎬 Endi kino kodini yuboring."
        )

    else:

        await callback.answer(
            "❌ Siz hali kanalga obuna bo'lmagansiz.",
            show_alert=True
        )