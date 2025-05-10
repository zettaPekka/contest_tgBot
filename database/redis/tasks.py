import asyncio

import secrets

from core.init_bot import bot
from database.cruds import get_users_by_contest, finish_contest, get_contest_by_id


async def bot_send_message(user_id: int, message: str):
    await bot.send_message(user_id, message)

async def async_finish_contest(contest_id: int):
    tasks = []
    
    users_id = await get_users_by_contest(contest_id)
    winer_index = secrets.randbelow(len(users_id))
    
    for index, user_id in enumerate(users_id):
        if index == winer_index:
            tasks.append(bot_send_message(user_id, f'Ты выиграл! {contest_id}'))
            winer_id = user_id
        else:
            tasks.append(bot_send_message(user_id, f'Розыгрыш окончен! Вы не выйграли. {contest_id}'))
    
    contest = await get_contest_by_id(contest_id)
    
    await bot.send_message(contest.user_id, f'Победитель в розыгрыше {contest_id}: {winer_id}')
    
    await asyncio.gather(*tasks, return_exceptions=True)
    await finish_contest(contest_id)

def finish_contest(contest_id: int):
    asyncio.run(async_finish_contest(contest_id))
