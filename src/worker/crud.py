from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from database.models import Worker, Arm, Inventory
from database.crud_base import CRUDBase

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
        log.debug(f"Debug --- get_worker_by_name name= {worker.name}")
        return worker

    # запросы к базе данных
    @staticmethod
    async def get_worker_arm(session: AsyncSession, username: str) -> Worker:
        """Получение компьютера работника"""
        query = (
            select(Worker.name, Arm.name)
            .select_from(Worker)
            .join(Arm, Worker.id == Arm.id)
            .where(Worker.name == username)
        )
        log.debug(f"Debug --- get_worker_arm query={query}")
        result = await session.execute(query)
        rows = result.fetchall()
        print(rows)
        if rows:
            result = [{"worker_name": row[0], "arm_name": row[1]} for row in rows]
            return result
        else:
            return []


class CRUDArm(CRUDBase):
    model = Arm


class CRUDInventory(CRUDBase):
    model = Inventory
