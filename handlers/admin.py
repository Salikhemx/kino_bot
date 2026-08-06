from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from config import ADMIN_ID
from database import (
    add_movie,
    get_all_users
)

router = Router()


class AddMovie(StatesGroup):
    video = State()
    code = State()


class Broadcast(StatesGroup):
    text = State()


# ==========================
# Kino qo'shish
# ==========================

@router.message(Command("add"))
async def add_cmd(message: Message, state: FSMContext):

    if message.from_user.id !=  8993879816
:
        await message.answer("❌ Siz admin emassiz!")
        return

    await message.answer("🎬 Videoni yuboring.")
    await state.set_state(AddMovie.video)


@router.message(AddMovie.video, F.video)
async def get_video(message: Message, state: FSMContext):

    await state.update_data(
        file_id=message.video.file_id
    )

    await message.answer(
        "🔢 Endi kino kodini yuboring."
    )

    await state.set_state(AddMovie.code)


@router.message(AddMovie.code)
async def save_movie(message: Message, state: FSMContext):

    data = await state.get_data()

    add_movie(
        message.text.strip(),
        data["file_id"]
    )

    await message.answer(
        "✅ Kino muvaffaqiyatli saqlandi."
    )

    await state.clear()


# ==========================
# Broadcast
# ==========================

@router.message(Command("broadcast"))
async def broadcast(message: Message, state: FSMContext):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "📢 Yubormoqchi bo'lgan xabaringizni yuboring."
    )

    await state.set_state(Broadcast.text)


@router.message(Broadcast.text)
async def send_broadcast(message: Message, state: FSMContext):

    users = get_all_users()

    success = 0
    failed = 0

    for user in users:

        try:

            await message.bot.send_message(
                user[0],
                message.text
            )

            success += 1

        except:

            failed += 1

    await message.answer(
        f"""
✅ Broadcast yakunlandi.

📨 Yuborildi: {success}

❌ Xato: {failed}
"""
    )

    await state.clear()