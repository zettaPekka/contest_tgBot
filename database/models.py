from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import JSON, BigInteger


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True)
    contests: Mapped[list[int]] = mapped_column(JSON, default=[])

class Contest(Base):
    __tablename__ = 'contests'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str]
    discription: Mapped[str]
    prize: Mapped[str]
    max_participants: Mapped[int]

