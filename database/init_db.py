from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv

import os

from database.models import Base


engine = create_async_engine(os.getenv('DB_PATH'))
async_session = async_sessionmaker(engine)


async def get_session():
    try:
        async with async_session() as session:
            yield session
    finally:
        await session.close()


class Database:
    def __init__(self):
        self.engine = create_async_engine(os.getenv('DB_PATH'))
        self.async_session = async_sessionmaker(self.engine)

class InitDatabase:
    def __init__(self, db: Database):
        self.db = db
    
    async def init_db(self):
        async with self.db.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)