from aiogram.fsm.state import State, StatesGroup


class CreateContest(StatesGroup):
    name = State()
    discription = State()
    prize = State()
    max_participants = State()
    days = State()
