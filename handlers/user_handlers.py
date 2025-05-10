from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from states.user_states import CreateContest
from database.cruds import add_user_if_not_exists, create_contest, take_part_in_contest, get_user_contests
from database.redis.add_contest import add_contest
from validate import check_message_type, check_digit


user_router = Router()


@user_router.message(CommandStart())
async def start(message: Message):
    await message.answer('<b>Привет! Если ты хочешь организовать честный розыгрыш, используй команду /create или нажми на кнопку ниже и я тебе помогу</b>')
    await add_user_if_not_exists(message.from_user.id)

'''
CREATE CONTEST
'''
@user_router.message(Command('create'))
async def create(message: Message, state: FSMContext):
    await message.answer('Создание состоит из нескольких частей... Введите название розыгрыша')
    await state.set_state(CreateContest.name)

@user_router.message(CreateContest.name)
async def get_name(message: Message, state: FSMContext):
    if not await check_message_type(message):
        return  
    await state.update_data(name=message.text)
    await message.answer('Введите описание розыгрыша')
    await state.set_state(CreateContest.discription)

@user_router.message(CreateContest.discription)
async def get_discription(message: Message, state: FSMContext):
    if not await check_message_type(message):
        return  
    await state.update_data(discription=message.text)
    await message.answer('Введите приз')
    await state.set_state(CreateContest.days)

@user_router.message(CreateContest.days)
async def get_discription(message: Message, state: FSMContext):
    if not await check_message_type(message):
        return  
    await state.update_data(days=message.text)
    await message.answer('Введите количество дней, в течение которых будет проходить розыгрыш')
    await state.set_state(CreateContest.prize)

@user_router.message(CreateContest.prize)
async def get_prize(message: Message, state: FSMContext):
    if not await check_message_type(message):
        return  
    await state.update_data(prize=message.text)
    await message.answer('Введите максимальное количество участников, которые могут участвовать в розыгрыше. Чтобы не указывать ограничения укажите -1')
    await state.set_state(CreateContest.max_participants)

@user_router.message(CreateContest.max_participants)
async def get_max_participants(message: Message, state: FSMContext):
    if not await check_digit(message):
        return  
    await state.update_data(max_participants=message.text)
    data = await state.get_data()
    contest = await create_contest(message.from_user.id, data['name'], data['discription'], data['prize'], int(data['max_participants']))
    await add_contest(contest.id, int(data['days']))
    await message.answer(f'Вы создали розыгрыш с названием: {data['name']}\nОписание: {data['discription']}\nПриз: {data['prize']}\nМаксимальное количество участников: {data['max_participants']}\nВремя: {data['days']} дней\n\nСсылка на участие в розыгрыше: t.me/{contest.id}')
    await state.clear()

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