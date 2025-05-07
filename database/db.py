from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from typing import AsyncIterator
from contextlib import asynccontextmanager

from database.models import Base


class DatabaseInitializer:
    def __init__(self, db_url: str):
        self._db_url = db_url
        self._engine = None

    async def init_db(self) -> None:
        self._engine = create_async_engine(self._db_url)
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @property
    def engine(self):
        if self._engine:
            return self._engine
        raise RuntimeError('Database is not initialized')


class SessionManager:
    def __init__(self, engine):
        self._engine = engine
        self._session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self._session_factory() as session:
            try:
                yield session
            finally:
                await session.close()