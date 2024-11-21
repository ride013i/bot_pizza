import asyncio
import datetime as dt
from typing import List

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker

from config import DB_URL

# Создаем движок и сессию
engine = create_async_engine(url=DB_URL, echo=True)
async_session = async_sessionmaker(engine)


# Базовый класс с поддержкой асинхронных атрибутов
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Класс пользователя
class User(Base):
    __tablename__ = "user"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    contact: Mapped[str]
    age: Mapped[int]
    effective_from_dttm: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now)

    # locations: Mapped[List["UserLocation"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    #
    def __repr__(self) -> str:
        return f"User(user_id={self.user_id}, name={self.name}, contact={self.contact}, age={self.age}, effective_from_dttm={self.effective_from_dttm})"


# Класс локации пользователя
class UserLocation(Base):
    __tablename__: str = "user_location"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    location: Mapped[str]
    effective_from_dttm: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now)

    # user: Mapped["User"] = relationship(back_populates="locations")
    #
    def __repr__(self) -> str:
        return f"UserLocation(id={self.id}, user_id={self.user_id}, location={self.location}, effective_from_dttm={self.effective_from_dttm})"


# Класс меню
class Menu(Base):
    __tablename__ = "menu"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    picture_id: Mapped[str]
    price: Mapped[str]
    effective_from_dttm: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now)

    def __repr__(self) -> str:
        return f"Menu(id={self.id}, name={self.name}, picture_id={self.picture_id}, price={self.price}, effective_from_dttm={self.effective_from_dttm})"


# Класс корзины
class Cart(Base):
    __tablename__ = "cart"
    id: Mapped[int] = mapped_column(primary_key=True)
    menu_id: Mapped[int] = mapped_column(ForeignKey("menu.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    name: Mapped[str]
    picture_id: Mapped[str]
    price: Mapped[str] = mapped_column(ForeignKey("menu.price"))
    effective_from_dttm: Mapped[dt.datetime] = mapped_column(default=dt.datetime.now)

    def __repr__(self) -> str:
        return f"Cart(id={self.id}, menu_id={self.menu_id}, user_id={self.user_id}, name={self.name}, picture_id={self.picture_id}, price={self.price}, effective_from_dttm={self.effective_from_dttm})"


# Асинхронная функция для создания таблиц в базе данных
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_user(user_id: int, name: str, contact: str, age: int):
    async with async_session() as session:
        async with session.begin():
            new_user = User(user_id=user_id, name=name, contact=contact, age=age)
            session.add(new_user)

async def add_user_location(user_id: int, location: str):
    async with async_session() as session:
        async with session.begin():
            new_location = UserLocation(user_id=user_id, location=location)
            session.add(new_location)

async def add_menu_item(name: str, picture_id: str, price: str):
    async with async_session() as session:
        async with session.begin():
            new_menu_item = Menu(name=name, picture_id=picture_id, price=price)
            session.add(new_menu_item)

async def add_to_cart(menu_id: int, user_id: int, name: str, picture_id: str, price: str):
    async with async_session() as session:
        async with session.begin():
            new_cart_item = Cart(
                menu_id=menu_id,
                user_id=user_id,
                name=name,
                picture_id=picture_id,
                price=price
            )
            session.add(new_cart_item)

# asyncio.run(add_menu_item())