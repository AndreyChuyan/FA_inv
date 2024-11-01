﻿from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///../db/inventory.db"  # Путь к вашей базе данных

engine = create_async_engine(DATABASE_URL)

# Базовый класс для моделей
Base = declarative_base()


# Создает асинхронный объект sessionmaker, который используется для создания сеанса работы с базой данных и выполнения асинхронных запросов.
async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with async_session() as session:
        yield session


# Функция для создания таблиц
async def create_tables():
    async with engine.begin() as conn:
        # Проверка наличия таблиц в базе данных
        inspector = inspect(conn)
        if not inspector.get_table_names():
            # Если таблицы отсутствуют, создаем их
            await conn.run_sync(Base.metadata.create_all)
        else:
            print("Таблицы уже существуют.")