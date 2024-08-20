from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import class_mapper
from fastapi import HTTPException
from .database import Base
from .models import Arm, Worker
from sqlalchemy import update, delete
from typing import List, TypeVar, Type
from sqlalchemy.orm import declarative_base, joinedload
import pandas as pd 


# отладка
import logging
log = logging.getLogger("uvicorn")

# Декларация Base
Base = declarative_base()
ModelType = TypeVar("ModelType", bound=Base)

class CRUDBase:
    model: Type[ModelType] = Base

    @classmethod
    async def get_all(cls, session: AsyncSession, order_by=None) -> list[model]:
        """Получение всех объектов"""
        query = select(cls.model)
        # log.debug(f'Debug --- get_all query={query}')
        if order_by:
            query = query.order_by(*order_by)
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
            # log.debug(f'Debug --- create error_info={error_info}')
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
            # log.debug(f"Debug --- worker_delete_by_id: Deleted worker with id= {id}")
            return True
        else:
            # log.debug(f"Debug --- worker_delete_by_id: No worker found with id= {id}")
            return False

    @classmethod
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
            # log.debug(f'Debug --- create error_info={error_info}')
            return None, error_info
        except NoResultFound:
            return None

    @classmethod
    async def get_all_arm_user(cls, session: AsyncSession, order_by=None) -> list[tuple]:
        """Получение всех объектов ARM с связанными пользователями"""
        query = select(Arm, Worker).join(Worker, Arm.id_worker == Worker.id)
        
        if order_by:
            query = query.order_by(*order_by)
        
        result = await session.execute(query)
        # log.debug(f'Debug --- get_all_arm_user result.scalars().all()= {result.scalars().all()}')
        return result.scalars().all()



class Exporter:
    @classmethod
    async def export_sqlite_to_excel(cls, session: AsyncSession, output_excel_file: str = "../export/export_db.xlsx"):
        try:
            async with session.begin():
                # Создаем Excel writer
                with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
                    # Экспортируем таблицу Worker
                    query = select(Worker)
                    result = await session.execute(query)
                    objects = result.scalars().all()
                    # log.debug(f'Debug --- export_sqlite_to_excel workers= {objects}')
                    # Преобразуем данные в DataFrame
                    data = [worker.as_dict() for worker in objects]
                    object_df = pd.DataFrame(data)
                    # log.debug(f'Debug --- export_sqlite_to_excel object_df= {object_df}')
                    object_df.to_excel(writer, sheet_name='Worker', index=False)

                    # Экспортируем таблицу Arm
                    query = select(Arm)
                    result = await session.execute(query)
                    objects = result.scalars().all()
                    # log.debug(f'Debug --- export_sqlite_to_excel workers= {objects}')
                    # Преобразуем данные в DataFrame
                    data = [arm.as_dict() for arm in objects]
                    object_df = pd.DataFrame(data)
                    # log.debug(f'Debug --- export_sqlite_to_excel object_df= {object_df}')
                    object_df.to_excel(writer, sheet_name='Arm', index=False)
            # Если всё прошло успешно
            return "Export_true"

        except Exception as e:
            # Если произошла ошибка
            return f"{str(e)}"

