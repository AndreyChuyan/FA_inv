from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from database.models import Worker, Arm, Inventory
from database.crud_base import CRUDBase
from sqlalchemy import update, delete


# отладка
import logging

log = logging.getLogger("uvicorn")


class CRUDArm(CRUDBase):
    model = Arm

    # @staticmethod
    # async def get_all_arm(session: AsyncSession) -> Arm:
    #     """Получение всех пользователей"""
    #     query = select(Arm)
    #     log.debug(f"Debug --- get_all query= {query}")
    #     result = await session.execute(query)
    #     objects = result.all()
    #     log.debug(f"Debug --- get_all objects= {objects}")
    #     return objects


    # @staticmethod
    # async def get_arm(session: AsyncSession, id: int) -> Worker:
    #     """Получение компьютера по имени пользователя"""
    #     query = select(Arm).filter(Arm.id == id)
    #     result = await session.execute(query)
    #     object = result.scalar_one_or_none()
    #     # log.debug(f"Debug --- get_worker_by_name worker.name= {worker.name}")
    #     return object

    @staticmethod
    async def arm_update_by_id(session: AsyncSession, id: int, data: dict) -> Worker:
        """Обновление компьютера по id"""
        # log.debug(f"Debug --- arm_update_by_id id, data= {id} {data}")
        query = (
            select(Arm)
            .filter(Arm.id == id)
            )
        result = await session.execute(query)
        object = result.scalar_one_or_none()
        if object is None:
            log.debug(f"Debug --- arm_update_by_id: No worker found with id= {id}")
            return None
        for key, value in data.items():
            setattr(object, key, value)
        await session.commit()
        log.debug(f"Debug --- arm_update_by_id: Updated worker id= {id}")
        return object
    
    @staticmethod
    async def arm_delete_by_id(session: AsyncSession, id: int) -> bool:
        """Удаление компьютера по id"""
        query = (
            delete(Arm)
            .where(Arm.id == id)
        )
        result = await session.execute(query)
        if result.rowcount == 1:
            await session.commit()
            log.debug(f"Debug --- arm_delete_by_id: Deleted arm with id= {id}")
            return True
        else:
            log.debug(f"Debug --- arm_delete_by_id: No arm found with id= {id}")
            return False



class CRUDInventory(CRUDBase):
    model = Inventory
