from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from database.models import Worker, Arm
from database.crud_base import CRUDBase
from sqlalchemy import update, delete


# отладка
import logging

log = logging.getLogger("uvicorn")


class CRUDWorker(CRUDBase):
    model = Worker

    @staticmethod
    async def get_worker_by_name(session: AsyncSession, name: str) -> Worker:
        """Получение пользователя по имени пользователя."""
        query = select(Worker).filter(Worker.name == name)
        result = await session.execute(query)
        worker = result.scalar_one_or_none()
        # log.debug(f"Debug --- get_worker_by_name worker.name= {worker.name}")
        return worker


    @classmethod
    async def get_all_worker_sorted(cls, session: AsyncSession) -> list[model]:
        """Получение всех компьютеров в сортировке"""
        order_by = [cls.model.fio]
        data = await cls.get_all(session, order_by=order_by)
        log.debug(f'Debug --- get_all_arm_sorted data={data}')
        return data



