from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified

from database.db import SessionManager
from database.models import User, Contest


class UserRepo:
    def __init__(self, db_session: SessionManager) -> None:
        self.db_session = db_session
    
    async def get_user(self, user_id: int) -> User | None:
        async with self.db_session.get_session() as session:
            user = await session.get(User, user_id)
            return user
    
    async def create_user(self, user_id: int) -> User:
        async with self.db_session.get_session() as session:
            user = await session.get(User, user_id)
            if not user:
                user = User(user_id=user_id)
                session.add(user)
                await session.commit()
                await session.refresh(user)
        return user
    
    async def get_user_contests(self, user_id: int) -> list[Contest]:
        async with self.db_session.get_session() as session:
            contests = await session.execute(
                select(Contest).where(Contest.user_id == user_id)
            )
            return contests.scalars().all()
    
    async def take_part_in_contest(self, user_id: int, contest_id: int) -> None:
        async with self.db_session.get_session() as session:
            user = await session.get(User, user_id)
            contest = await session.get(Contest, contest_id)
            if not contest:
                raise ValueError('Contest not found')
            if user in contest.participants:
                raise ValueError('User already in contest')
            if contest.max_participants != -1 and len(contest.participants) >= contest.max_participants:
                raise ValueError('Contest is full')
            user.contests.append(contest)
            contest.participants.append(user)
            flag_modified(contest, 'participants')
            await session.commit()
            return contest

class ContestRepo:
    def __init__(self, db_session: SessionManager) -> None:
        self.db_session = db_session

    async def create_contest(self, user_id: int, name: str, discription: str, prize: str, max_participants: int) -> Contest:
        async with self.db_session.get_session() as session:
            contest = Contest(user_id=user_id, name=name, discription=discription, prize=prize, max_participants=max_participants)
            session.add(contest)
            await session.commit()
            await session.refresh(contest)
        return contest

    async def get_contest(self, contest_id: int) -> Contest | None:
        async with self.db_session.get_session() as session:
            contest = await session.get(Contest, contest_id)
            return contest
    
    async def edit_contest(self, option: str) -> Contest:
        ...
    
    async def delete_contest(self, contest_id: int) -> None:
        async with self.db_session.get_session() as session:
            contest = await session.get(Contest, contest_id)
            await session.delete(contest)
            await session.commit()
            return contest