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

