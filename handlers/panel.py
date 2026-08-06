from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import ADMIN_ID
from database import set_channel, get_channel

router = Router()


class ChannelState(StatesGroup):
    waiting_channel = State()


panel_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="➕ Kanal qo'shish"),
            KeyboardButton(text="📋 Kanalni ko'rish")
        ],
        [
            KeyboardButton(text="🎬 Kino qo'shish"),
            KeyboardButton(text="📊 Statistika")
        ]
    ],
    resize_keyboard=True
)


@router.message(Command("panel"))
async def panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Siz admin emassiz!")
        return

    await message.answer(
        "⚙️ Admin panelga xush kelibsiz.",
        reply_markup=panel_keyboard
    )


@router.message(F.text == "➕ Kanal qo'shish")
async def add_channel(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "📢 Kanal username yuboring.\n\n"
        "Misol:\n"
        "@kinolar12026"
    )

    await state.set_state(ChannelState.waiting_channel)


@router.message(ChannelState.waiting_channel)
async def save_channel(message: Message, state: FSMContext):
    if not message.text.startswith("@"):
        await message.answer(
            "❌ Username @ bilan boshlanishi kerak."
        )
        return

    set_channel(message.text)

    await message.answer(
        f"✅ Kanal saqlandi:\n{message.text}"
    )

    await state.clear()


@router.message(F.text == "📋 Kanalni ko'rish")
async def show_channel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    channel = get_channel()

    if channel:
        await message.answer(
            f"📢 Hozirgi kanal:\n{channel}"
        )
    else:
        await message.answer(
            "❌ Hali kanal qo'shilmagan."
        )


@router.message(F.text == "📊 Statistika")
async def statistic(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "📊 Statistika bo'limi hali tayyor emas."
    )


@router.message(F.text == "🎬 Kino qo'shish")
async def movie_add(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "🎬 Kino qo'shish uchun /add buyrug'idan foydalaning."
    )