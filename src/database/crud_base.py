from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException
from .database import Base
from .models import Arm, Worker
from sqlalchemy import update, delete

# отладка
import logging
log = logging.getLogger("uvicorn")

class CRUDBase:
    model: Base = Base

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[model]:
        """Получение всех объектов"""
        query = select(cls.model)
        # log.debug(f'Debug --- get_all query={query}')
        result = await session.execute(query)
        return result.scalars().all()

    # для создания нового объекта model и его сохранения в базе данных через асинхронный сеанс session
    @classmethod
    async def create(cls, session: AsyncSession, data: dict) -> tuple[model | None, str | None]:
        """Создание нового объекта"""
        try:
            obj = cls.model(**data)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj, None
        except IntegrityError as e:
            await session.rollback()
            error_info = str(e.orig)
            log.debug(f'Debug --- create error_info={error_info}')
            return None, error_info

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id: int) -> model | None:
        """Получение объекта по ID"""
        query = select(cls.model).filter(cls.model.id == id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, id: int) -> None:
        """Удаление объекта по ID"""
        query = delete(cls.model).where(cls.model.id == id)
        result = await session.execute(query)
        if result.rowcount == 1:
            await session.commit()
            log.debug(f"Debug --- worker_delete_by_id: Deleted worker with id= {id}")
            return True
        else:
            log.debug(f"Debug --- worker_delete_by_id: No worker found with id= {id}")
            return False

    @classmethod
    
        # async def update_by_id(cls, session: AsyncSession, id: int, data: dict) -> model | None:
        # """Обновление существующего объекта по ID"""
        # try:
        #     obj = await session.get(cls.model, id)
        #     if not obj:
        #         return None
        #     for key, value in data.items():
        #         setattr(obj, key, value)
        #     await session.commit()
        #     await session.refresh(obj)
        #     return obj
        # except IntegrityError:
        #     await session.rollback()
        #     return None
        # except NoResultFound:
        #     return None
    
    async def update_by_id(cls, session: AsyncSession, id: int, data: dict) -> model | None:
        """Обновление существующего объекта по ID"""
        try:
            obj = await session.get(cls.model, id)
            if not obj:
                return None
            for key, value in data.items():
                if key == "password" and value is None:
                    continue  # Пропускаем обновление пароля, если он не предоставлен
                setattr(obj, key, value)
            await session.commit()
            await session.refresh(obj)
            return obj, None
        except IntegrityError as e:
            await session.rollback()
            error_info = str(e.orig)
            log.debug(f'Debug --- create error_info={error_info}')
            return None, error_info
        except NoResultFound:
            return None
        