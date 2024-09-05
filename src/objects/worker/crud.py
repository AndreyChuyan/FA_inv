from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from database.models import Worker, Arm
from database.crud_base import CRUDBase
from sqlalchemy import update, delete
from sqlalchemy import distinct

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
        # log.debug(f'Debug --- get_all_arm_sorted data={data}')
        return data

    @classmethod
    async def delete_worker_and_update_arms(cls, session: AsyncSession, worker_id: int) -> bool:
        """
        Удаление объекта Worker по ID и обновление связанных записей Arm
        """
        try:
            # Обновление записей Arm, связанных с удаляемым Worker
            update_query = update(Arm).where(Arm.id_worker == worker_id).values(id_worker=0)
            await session.execute(update_query)

            # Удаление Worker
            delete_query = delete(Worker).where(Worker.id == worker_id)
            result = await session.execute(delete_query)

            if result.rowcount == 1:
                await session.commit()
                # log.debug(f"Debug --- delete_worker_and_update_arms: Deleted worker with id={worker_id} and updated related Arms")
                return True
            else:
                await session.rollback()
                # log.debug(f"Debug --- delete_worker_and_update_arms: No worker found with id={worker_id}")
                return False

        except Exception as e:
            await session.rollback()
            # log.error(f"Error --- delete_worker_and_update_arms: Failed to delete worker with id={worker_id}. Error: {str(e)}")
            return False

    # @classmethod
    # async def get_worker_unique_departments(cls, session: AsyncSession) -> list[str]:
    #     """Получение уникальных подразделений"""
    #     # Используем distinct для выбора уникальных значений
    #     query = select(distinct(cls.model.department)).order_by(cls.model.department)
        
    #     result = await session.execute(query)
    #     data = result.scalars().all()
    #     return data
