from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import BigInteger, Integer, String, Boolean, Float
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3", echo = True)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    telegram_id = Column(String)
    balance = Column(Float)
    subscribe = Column(Integer)




async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    