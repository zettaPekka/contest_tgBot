from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext


user_router = Router()


@user_router.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет!')

