from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from .database import Base
from .models import Arm, Worker, Inventory
from sqlalchemy import update

class CRUDBase:
    model: Base = Base
    
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
    async def get_all(cls, session: AsyncSession) -> list[model]:
        """Получение всех объектов"""
        query = select(cls.model)
        result = await session.execute(query)
        return result.scalars().all()
      
    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int) -> model | None:
        """Получение объекта по ID"""
        query = select(cls.model).filter(cls.model.id == id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
      
    