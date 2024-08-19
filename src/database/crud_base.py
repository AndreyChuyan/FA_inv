from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException
from .database import Base
from .models import Arm, Worker
from sqlalchemy import update, delete
from typing import List, TypeVar, Type
from sqlalchemy.orm import declarative_base
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
        
    @classmethod
    async def export_sqlite_to_excel(cls, session: AsyncSession, output_excel_file: str = "./export_db.xlsx"):
        async with session.begin():
            # Выполняем асинхронный запрос к базе данных для получения всех имен таблиц
            # result = await session.execute(select(["name"]).select_from("sqlite_master").where("type='table'"))
            result = select(cls.model)
            tables = [row[0] for row in result.fetchall()]

            # Создаем Excel файл
            with pd.ExcelWriter(output_excel_file, engine='xlsxwriter') as writer:
                # Экспортируем данные каждой таблицы в отдельный лист Excel
                for table in tables:
                    # Используем синхронный метод для чтения данных из таблицы
                    query = f'SELECT * FROM {table}'
                    df = pd.read_sql(query, session.bind)
                    df.to_excel(writer, sheet_name=table)

            print(f"Данные успешно экспортированы в {output_excel_file}")
            return {"message": "Export successful", "file": output_excel_file}