from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from database.models import Worker, Arm, Inventory
from database.crud_base import CRUDBase

class CRUDWorker(CRUDBase):
    model = Worker
    
    @staticmethod
    async def get_worker_by_name(session: AsyncSession, name: str) -> Worker:
        """Получение пользователя по имени пользователя."""
        query = select(Worker).filter(Worker.name == name)
        result = await session.execute(query)
        worker = result.scalar_one_or_none()
        return worker    

class CRUDArm(CRUDBase):
    model = Arm
    
class CRUDInventory(CRUDBase):
    model = Inventory
    

