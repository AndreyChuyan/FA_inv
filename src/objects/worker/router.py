from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse, Response

from database.database import get_session
from database.models import Worker
from .schemas import WorkerCreate, WorkerOut, WorkerForm
from .crud import CRUDWorker
from .dependency import get_current_worker, get_worker_by_id

from .auth import hash_password, verify_password, create_access_token
from .exceptions import exception_user_not_found, exception_auth
from exception import DuplicateObjectException

# отладка
import logging

log = logging.getLogger("uvicorn")

router = APIRouter(prefix="/worker", tags=["worker"])


# --- Авторизация
@router.post("/token")
async def fio_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    worker = await CRUDWorker.get_worker_by_name(session, form_data.username)
    if not worker or not verify_password(form_data.password, worker.password):
        raise exception_auth
    access_token = create_access_token(data={"sub": worker.name})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth")
async def fio_for_access_token_frontend(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await CRUDWorker.get_worker_by_name(session, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        return RedirectResponse(
            url="/auth?not_auth=true", status_code=status.HTTP_303_SEE_OTHER
        )
    access_token = create_access_token(data={"sub": user.name})
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token)
    return response


@router.post("/", response_model=WorkerOut, status_code=status.HTTP_201_CREATED)
async def create(
    user: WorkerCreate, 
    session: AsyncSession = Depends(get_session),
    # current_user: Worker = Depends(get_current_worker),
    ):
    """
    Создание нового пользователя.
    """
    user.password = hash_password(user.password)
    data = user.dict()
    worker = data.pop("worker", None)
    new_user, error_info = await CRUDWorker.create(session, data)
    if new_user is None:
        log.debug(f'Debug --- router create - error_info {error_info}')
        if "UNIQUE constraint failed: worker.name" in error_info:
            raise DuplicateObjectException("UNIQUE constraint failed: worker.name")
        else:
        # Обработка других типов ошибок
            raise HTTPException(status_code=400, detail="Failed to create user")
    # if worker:
    #     user["id"] = new_user.id
    #     await CRUDWorker.create(session, worker)
    log.info(f'Создан пользователь Логин= {new_user.name} Имя= {new_user.fio}')
    return new_user

@router.get("/{worker_id}", response_model=WorkerOut)
async def get_user(
    worker: Worker = Depends(get_worker_by_id),
    session: AsyncSession = Depends(get_session),
    # current_user: Worker = Depends(get_current_worker),
):
    """
    Получение информации о пользователе по ID.
    """
    return worker


@router.get("/", response_model=list[WorkerOut])
async def get_all(
    session: AsyncSession = Depends(get_session),
    current_user: Worker = Depends(get_current_worker),
    ):
    """
    Получение списка всех пользователей.
    """
    users = await CRUDWorker.get_all(session)
    # log.debug(f'Debug --- get_all_worker')

    return users


@router.put("/{id}", response_model=WorkerOut)
async def update_by_id(
    id: int,
    user: WorkerForm, 
    session: AsyncSession = Depends(get_session),
    # current_user: Worker = Depends(get_current_worker),
):
    """
    Обновление пользователя
    """
    # если пароль не введен в форму - он в базе данных не меняется
    if user.password == "":
        user.password = None
    else:
        user.password = hash_password(user.password)
    # log.debug(f'Debug --- worker_update_by_id user.password={user.password}')
    data = user.dict()
    user, error_info = await CRUDWorker.update_by_id(session, id, data)
    # log.debug(f'Debug --- worker_update_by_id session, id, data= {session} {id} {data}')
    if user is None:
        # log.debug(f'Debug --- router create - error_info {error_info}')
        if "UNIQUE constraint failed: worker.name" in error_info:
            raise DuplicateObjectException("UNIQUE constraint failed: worker.name")
        else:
        # Обработка других типов ошибок
            raise HTTPException(status_code=400, detail="Failed to create user")
    return user

@router.delete("/{id}", response_model=bool)
async def delete_by_id(
    id: int,
    session: AsyncSession = Depends(get_session),
    # current_user: Worker = Depends(get_current_worker),
):
    """
    Удаление пользователя по ID
    """
    success = await CRUDWorker.delete_worker_and_update_arms(session, id)
    return success