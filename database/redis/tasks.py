import asyncio


async def async_finish_contest(contest_id: int):
    print('contest finished', contest_id)

def finish_contest(contest_id: int):
    asyncio.run(async_finish_contest(contest_id))
