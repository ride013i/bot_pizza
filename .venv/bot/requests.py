import asyncio

from sqlalchemy import select, insert, update, desc, delete

from models import async_session
from models import User, UserLocation, Menu, Cart

# Получить все меню
async def get_menu():
    async with async_session() as session:
        return await session.scalars(select(Menu))

# Получить все telegram id
async def get_user_id(user_id):
    async with async_session() as session:
        return await session.scalar(select(User.user_id).where(User.user_id == user_id))

# Получить все меню
async def get_profile(user_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.user_id == user_id))

# Получить Всю корзину пользователя
async def get_cart(user_id):
    async with async_session() as session:
        return await session.scalars(select(Cart).where(Cart.user_id == user_id))

# Получить Пиццу
async def get_item(menu_id):
    async with async_session() as session:
        return await session.scalar(select(Menu).where(Menu.id == menu_id))

# print(asyncio.run(get_user_id('113546447')))