from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from config import ADMIN_ID
from database import add_movie

router = Router()


class AddMovie(StatesGroup):
    video = State()
    code = State()


@router.message(Command("add"))
async def add_cmd(message: Message, state: FSMContext):
    await message.answer(
        f"Sizning ID: {message.from_user.id}\nADMIN_ID: {ADMIN_ID}"
    )

    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Siz admin emassiz!")
        return

    await message.answer("🎬 Videoni yuboring.")
    await state.set_state(AddMovie.video)


@router.message(AddMovie.video, F.video)
async def get_video(message: Message, state: FSMContext):
    await state.update_data(file_id=message.video.file_id)
    await message.answer("🔢 Endi kino kodini yuboring.")
    await state.set_state(AddMovie.code)


@router.message(AddMovie.code)
async def save_movie(message: Message, state: FSMContext):
    data = await state.get_data()

    add_movie(
        message.text.strip(),
        data["file_id"]
    )

    await message.answer("✅ Kino saqlandi!")
    await state.clear()