from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse, Response
from .exceptions import exception_user_not_found, exception_auth, exception_unique_field

from database.database import get_session
from database.models import Arm, Worker
from .schemas import ArmBase, ArmOut, ArmForm
from .crud import CRUDArm
from database.crud_base import CRUDBase
from objects.worker.dependency import get_current_worker
from exception import DuplicateObjectException

# отладка
import logging

log = logging.getLogger("uvicorn")

router = APIRouter(prefix="/arm", tags=["arm"])

# --- Standart CRUD
@router.post("/", response_model=ArmOut, status_code=status.HTTP_201_CREATED)
async def create(
    arm: ArmBase, 
    session: AsyncSession = Depends(get_session),
    
    ):
    """
    Создание нового пользователя.
    """
    data = arm.dict()
    object = data.pop("arm", None)
    object_resp, error_info = await CRUDArm.create(session, data)
    # обработка ошибки
    if object_resp is None:
        if "UNIQUE constraint failed: arm.title" in error_info:
            raise DuplicateObjectException("UNIQUE constraint failed: arm.title")
        else:
        # Обработка других типов ошибок
            raise HTTPException(status_code=400, detail="Failed to create arm")
    if object:
        arm["id"] = object_resp.id
        await CRUDArm.create(session, object)
    return object_resp


@router.get("/{worker_id}", response_model=ArmOut)
async def get_by_id(
    id: int,
    session: AsyncSession = Depends(get_session),
):
    """
    Получение информации о пользователе по ID.
    """
    object = await CRUDArm.get_by_id(session, id)
    # log.debug(f'Debug --- get_arm_by_id object={object}')
    return object


@router.get("/", response_model=list[ArmOut])
async def get_all(
    session: AsyncSession = Depends(get_session),
    current_user: Worker = Depends(get_current_worker),
    ):
    """
    Получение списка всех пользователей.
    """
    object = await CRUDArm.get_all(session)
    # log.debug(f'Debug --- get_all_arm users={object}')
    return object


@router.put("/{id}", response_model=ArmOut)
async def update_by_id(
    id: int,
    schema: ArmForm, 
    session: AsyncSession = Depends(get_session)
):
    """
    Обновление компьютера
    """
    # log.debug(f'Debug --- arm_update_by_id object.name={schema.name}')
    data = schema.dict()
    object = await CRUDArm.update_by_id(session, id, data)
    # log.debug(f'Debug --- worker_update_by_id session, id, data= {session} {id} {data}')
    return object

@router.delete("/{id}", response_model=bool)
async def delete_by_id(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Удаление компьютера по ID
    """
    success = await CRUDArm.delete_by_id(session, id)
    return success