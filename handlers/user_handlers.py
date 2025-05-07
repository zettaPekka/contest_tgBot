from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from states.user_states import CreateContest


user_router = Router()


@user_router.message(CommandStart())
async def start(message: Message):
    await message.answer('<b>Привет! Если ты хочешь организовать честный розыгрыш, используй команду /create или нажми на кнопку ниже и я тебе помогу</b>')



'''
CREATE CONTEST
'''
@user_router.message(Command('create'))
async def create(message: Message, state: FSMContext):
    await message.answer('Создание состоит из нескольких частей... Введите название розыгрыша')
    await state.set_state(CreateContest.name)

@user_router.message(CreateContest.name)
async def get_name(message: Message, state: FSMContext):
    '''проверка'''
    await state.update_data(name=message.text)
    await message.answer('Введите описание розыгрыша')
    await state.set_state(CreateContest.discription)

@user_router.message(CreateContest.discription)
async def get_discription(message: Message, state: FSMContext):
    '''проверка'''
    await state.update_data(discription=message.text)
    await message.answer('Введите приз')
    await state.set_state(CreateContest.prize)

@user_router.message(CreateContest.prize)
async def get_prize(message: Message, state: FSMContext):
    '''проверка'''
    await state.update_data(prize=message.text)
    await message.answer('Введите максимальное количество участников, которые могут участвовать в розыгрыше. Чтобы не указывать ограничения укажите -1')
    await state.set_state(CreateContest.max_participants)

@user_router.message(CreateContest.max_participants)
async def get_max_participants(message: Message, state: FSMContext):
    '''проверка'''
    await state.update_data(max_participants=message.text)
    data = await state.get_data()
    await message.answer(f'Вы создали розыгрыш с названием: {data["name"]}\nОписание: {data["discription"]}\nПриз: {data["prize"]}\nМаксимальное количество участников: {data["max_participants"]}')
'''
EDIT/DELETE CONTEST
'''
@user_router.message(Command('edit'))
async def edit(message: Message):
    await message.answer('Выберите розыгрыш, который хотите изменить')

@user_router.message(Command('delete'))
async def delete(message: Message):
    await message.answer('Выберите розыгрыш, который хотите изменить')
'''
USER DATA
'''
@user_router.message(Command('me'))
async def user_data(message: Message):
    await message.answer('Ваши розыгрыши: ...')