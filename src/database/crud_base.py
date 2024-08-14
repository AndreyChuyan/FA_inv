from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from .database import Base
from .models import Arm, Worker, Inventory
from sqlalchemy import update

# отладка
import logging
log = logging.getLogger("uvicorn")

class CRUDBase:
    model: Base = Base

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[model]:
        """Получение всех объектов"""
        query = select(cls.model)
        log.debug(f'Debug --- get_all query={query}')
        result = await session.execute(query)
        return result.scalars().all()

    # для создания нового объекта model и его сохранения в базе данных через асинхронный сеанс session
    @classmethod
    async def create(cls, session: AsyncSession, data: dict) -> model | None:
        """Создание нового объекта"""
        try:
            obj = cls.model(**data)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj
        except IntegrityError:
            await session.rollback()
            return None

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int) -> model | None:
        """Получение объекта по ID"""
        query = select(cls.model).filter(cls.model.id == id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    # @classmethod
    # async def update_by_id(cls, session: AsyncSession, id: int, update_data: dict) -> model | None:
    #     """Обновление объекта по ID"""
    #     try:
    #         # Найти объект по ID
    #         query = select(cls.model).filter(cls.model.id == id)
    #         result = await session.execute(query)
    #         if result is None:
    #             return None
    #         # Обновить атрибуты объекта на основе переданных данных
    #         for key, value in update_data.items():
    #             setattr(result, key, value)
    #         await session.commit()
    #         return result
    #     except IntegrityError:
    #         await session.rollback()
    #         return None
        