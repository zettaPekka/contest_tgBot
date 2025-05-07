from database.db import SessionManager
from database.models import User


class UserRepo:
    def __init__(self, db_session: SessionManager):
        self.db_session = db_session
    
    async def get_user(self, user_id: int) -> dict | None:
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