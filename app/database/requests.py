from app.database.models import async_session, User
from sqlalchemy import select


async def create_user(telegram_id):
    async with async_session() as session:
        session.add(User(telegram_id=telegram_id, balance = 0, subscribe = 0))
        await session.commit()


async def check_user(telegram_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        if user:
            return True
        return False
    
async def add_balance(telegram_id: str, amount: float):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        user.balance += amount
        await session.commit()

async def check_balance(telegram_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        return user.balance
    

async def add_subscribe(telegram_id, subscribe: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        user.subscribe += subscribe
        await session.commit()

async def remove_subscribe(telegram_id, subscribe: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        user.subscribe -= subscribe
        await session.commit()


async def check_subscribe(telegram_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        if(int(user.subscribe) > 0):
            return user.subscribe
        else:
            return 0



        