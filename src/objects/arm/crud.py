from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from database.models import Worker, Arm
from database.crud_base import CRUDBase
from sqlalchemy import update, delete


# отладка
import logging

log = logging.getLogger("uvicorn")


class CRUDArm(CRUDBase):
    model = Arm

    @classmethod
    async def get_all_arm_sorted(cls, session: AsyncSession) -> list[model]:
        """Получение всех компьютеров в сортировке"""
        order_by = [cls.model.department_arm]
        data = await cls.get_all(session, order_by=order_by)
        # log.debug(f'Debug --- get_all_arm_sorted data={data}')
        return data
    
