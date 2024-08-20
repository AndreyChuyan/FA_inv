from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse, Response
from .exceptions import exception_user_not_found, exception_auth, exception_unique_field

from database.database import get_session
from database.models import Inventory
from .schemas import InventoryBase, InventoryOut, InventoryForm
from .crud import CRUDInventory
from database.crud_base import CRUDBase


# отладка
import logging

log = logging.getLogger("uvicorn")

router = APIRouter(prefix="/inventory", tags=["inventory"])

# --- Standart CRUD
@router.post("/", response_model=InventoryOut, status_code=status.HTTP_201_CREATED)
async def create(inventory: InventoryBase, session: AsyncSession = Depends(get_session)):
    """
    Создание нового пользователя.
    """
    data = inventory.dict()
    object = data.pop("inventory", None)
    object_resp = await CRUDInventory.create(session, data)
    if object_resp is None:
        raise exception_unique_field
    if object:
        inventory["id"] = object_resp.id
        await CRUDInventory.create(session, object)
    return object_resp


@router.get("/{inventory_id}", response_model=InventoryBase)
async def get_by_id(
    id: int,
    session: AsyncSession = Depends(get_session),
):
    """
    Получение информации о пользователе по ID.
    """
    object = await CRUDInventory.get_by_id(session, id)
    # log.debug(f'Debug --- get_inventory_by_id object={object}')
    return object


@router.get("/", response_model=list[InventoryOut])
async def get_all(session: AsyncSession = Depends(get_session)):
    """
    Получение списка всех пользователей.
    """
    object = await CRUDInventory.get_all(session)
    # log.debug(f'Debug --- get_all_inventory users={object}')
    return object


@router.put("/{id}", response_model=InventoryOut)
async def update_by_id(
    id: int,
    schema: InventoryForm, 
    session: AsyncSession = Depends(get_session)
):
    """
    Обновление компьютера
    """
    data = schema.dict()
    object = await CRUDInventory.update_by_id(session, id, data)
    # log.debug(f'Debug --- inventory_update_by_id session, id, data= {session} {id} {data}')
    return object

@router.delete("/{id}", response_model=bool)
async def delete_by_id(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Удаление инвента по ID
    """
    success = await CRUDInventory.delete_by_id(session, id)
    return success