from app.database.models import async_session, User, Promocode
from sqlalchemy import select


async def add_promocode(telegram_id: str, promocode: str):
    async with async_session() as session:
        session.add(Promocode(telegram_id = telegram_id, promocode = promocode))
        await session.commit()

async def check_promocode(telegram_id: str, promocode: str):
    async with async_session() as session:
        promo = await session.scalar(select(Promocode).where(Promocode.promocode == promocode and Promocode.telegram_id == telegram_id))
        if promo:
            print(f"PROMOCODE : {promo.promocode}")
            return True
        else:
            return False

async def create_user(telegram_id):
    async with async_session() as session:
        session.add(User(telegram_id=telegram_id, balance = 0, subscribe = 0, current_stavka = 0))
        await session.commit()


async def set_stavka(telegram_id, stavka):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.telegram_id == telegram_id))
        user.current_stavka = stavka
        await session.commit()


async def get_stavka(telegram_id):
    async with async_session() as session:
        print(f"ID: {telegram_id}")
        user = await session.scalar(select(User).where(User.telegram_id == str(telegram_id)))
        return user.current_stavka

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



        