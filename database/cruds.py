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
        user = await session.get(User, user_id)
        if user:
            user.contests.append(contest.id)
            flag_modified(user, 'contests') 
        
        await session.commit()
        await session.refresh(contest)
    return contest

async def take_part_in_contest(user_id: int, contest_id: int) -> dict:
    async with async_session() as session:
        contest = await session.get(Contest, contest_id)
        print(contest, contest_id)
        if contest:
            if user_id not in contest.participants and len(contest.participants) < contest.max_participants:
                contest.participants.append(user_id)
                user = await session.get(User, user_id)
                user.in_contests.append(contest_id)
                
                flag_modified(user, 'in_contests')
                flag_modified(contest, 'participants')
                await session.commit()
                return {'status': True, 'contest': contest}
            return {'status': False, 'error': 'Вы уже учавствуете в этом конкурсе'}
        return {'status': False, 'error': 'Розыгрыш не найден, возможно он уже завершен'}

async def get_created_contests(user_id: int) -> list:
    async with async_session() as session:
        contests = await session.execute(select(Contest).where(Contest.user_id == user_id))
        return contests.scalars().all()

async def get_contests_by_participant(user_id: int) -> list:
    async with async_session() as session:
        contests = await session.execute(select(Contest).where(Contest.participants.contains(user_id)))
        return contests.scalars().all()

async def get_users_by_contest(contest_id: int) -> list:
    async with async_session() as session:
        contest = await session.get(Contest, contest_id)
        return contest.participants

async def finish_contest(contest_id: int) -> None:
    async with async_session() as session:
        contest = await session.get(Contest, contest_id)
        await session.delete(contest)
        await session.commit()

async def get_contest_by_id(contest_id: int) -> Contest | None:
    async with async_session() as session:
        contest = await session.get(Contest, contest_id)
        return contest