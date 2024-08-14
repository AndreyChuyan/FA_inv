from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from database.models import Worker, Arm, Inventory
from database.crud_base import CRUDBase
from sqlalchemy import update, delete


# отладка
import logging

log = logging.getLogger("uvicorn")


class CRUDWorker(CRUDBase):
    model = Worker

    @staticmethod
    async def get_all(session: AsyncSession, name: str) -> Worker:
        """Получение всех пользователей"""
        query = select(Worker)
        result = await session.execute(query)
        worker = result.all()
        log.debug(f"Debug --- get_all worker= {worker}")
        return worker

    @staticmethod
    async def get_worker_by_name(session: AsyncSession, name: str) -> Worker:
        """Получение пользователя по имени пользователя."""
        query = select(Worker).filter(Worker.name == name)
        result = await session.execute(query)
        worker = result.scalar_one_or_none()
        # log.debug(f"Debug --- get_worker_by_name worker.name= {worker.name}")
        return worker

    @staticmethod
    async def worker_update_by_id(session: AsyncSession, id: int, data: dict) -> Worker:
        """Обновление сотрудника по id"""
        # log.debug(f"Debug --- worker_update_by_id id, data= {id} {data}")
        query = (
            select(Worker)
            .filter(Worker.id == id)
            )
        result = await session.execute(query)
        worker = result.scalar_one_or_none()
        if worker is None:
            log.debug(f"Debug --- worker_update_by_id: No worker found with id= {id}")
            return None
        for key, value in data.items():
            setattr(worker, key, value)
        await session.commit()
        log.debug(f"Debug --- worker_update_by_id: Updated worker id= {id}")
        return worker
    
    @staticmethod
    async def worker_delete_by_id(session: AsyncSession, id: int) -> bool:
        """Удаление сотрудника по id"""
        query = (
            delete(Worker)
            .where(Worker.id == id)
        )
        result = await session.execute(query)
        if result.rowcount == 1:
            await session.commit()
            log.debug(f"Debug --- worker_delete_by_id: Deleted worker with id= {id}")
            return True
        else:
            log.debug(f"Debug --- worker_delete_by_id: No worker found with id= {id}")
            return False


class CRUDArm(CRUDBase):
    model = Arm


class CRUDInventory(CRUDBase):
    model = Inventory
