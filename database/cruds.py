from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import select

from database.models import Contest, User
from database.init_db import engine


async_session = async_sessionmaker(bind=engine)


async def add_user_if_not_exists(user_id: int) -> None:
    async with async_session() as session:
        user = await session.get(User, user_id)
        if not user:
            user = User(user_id=user_id)
            session.add(user)
            await session.commit()

async def create_contest(user_id: int, name: str, discription: str, prize: str, max_participants: int) -> Contest:
    async with async_session() as session:
        contest = Contest(user_id=user_id, name=name, discription=discription, prize=prize, max_participants=max_participants)
        session.add(contest)
        await session.commit()
        await session.refresh(contest)
    return contest

async def take_part_in_contest(user_id: int, contest_id: int) -> bool:
    async with async_session() as session:
        contest = await session.get(Contest, contest_id)
        if contest:
            if user_id not in contest.participants:
                contest.participants.append(user_id)
                flag_modified(contest, 'participants')
                await session.commit()
                return {'status': True}
            return {'status': False, 'error': 'already in the contest'}
    return {'status': False, 'error': 'not found'}

async def get_user_contests(user_id: int) -> list:
    async with async_session() as session:
        contests = await session.execute(select(Contest).where(Contest.user_id == user_id))
        return contests.scalars().all()
