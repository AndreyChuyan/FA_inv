from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse, Response

from database.database import get_session
from database.models import Arm
from .schemas import ArmCreate, ArmOut, ArmForm
from .crud import CRUDWorker


from .auth import hash_password, verify_password, create_access_token
from .exceptions import exception_user_not_found, exception_auth, exception_unique_field

# отладка
import logging

log = logging.getLogger("uvicorn")

router = APIRouter(prefix="/worker", tags=["worker"])


# --- Авторизация
@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    worker = await CRUDWorker.get_worker_by_name(session, form_data.username)
    if not worker or not verify_password(form_data.password, worker.password):
        raise exception_auth
    access_token = create_access_token(data={"sub": worker.name})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth")
async def login_for_access_token_frontend(
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


# @router.post("/register")
# async def register_user(
#     name: str = Form(...),
#     password: str = Form(...),
#     email: str = Form(...),
#     session: AsyncSession = Depends(get_session),
# ):
#     password = hash_password(password)
#     data = {"username": username, "password": password, "email": email}
#     user = await CRUDUser.create(session, data)
#     access_token = create_access_token(data={"username": user.username})
#     # print(access_token)repod1
#     response = RedirectResponse(url="/auth", status_code=status.HTTP_303_SEE_OTHER)
#     response.set_cookie(key="access_token", value=access_token)
#     return response

# --- Standart CRUD
@router.post("/", response_model=WorkerOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: WorkerCreate, session: AsyncSession = Depends(get_session)):
    """
    Создание нового пользователя.
    """
    user.password = hash_password(user.password)
    data = user.dict()
    worker = data.pop("worker", None)
    new_user = await CRUDWorker.create(session, data)
    if new_user is None:
        raise exception_unique_field
    if worker:
        user["id"] = new_user.id
        await CRUDWorker.create(session, worker)
    return new_user


@router.get("/{worker_id}", response_model=WorkerOut)
async def get_user(
    worker: Worker = Depends(get_worker_by_id),
    session: AsyncSession = Depends(get_session),
    current_user: Worker = Depends(get_current_worker),
):
    """
    Получение информации о пользователе по ID.
    """
    return worker


@router.get("/", response_model=list[WorkerOut])
async def get_all_worker(session: AsyncSession = Depends(get_session)):
    """
    Получение списка всех пользователей.
    """
    users = await CRUDWorker.get_all(session)
    # log.debug(f'Debug --- get_all_worker')
    return users


@router.put("/{id}", response_model=WorkerOut)
async def worker_update_by_id(
    id: int,
    user: WorkerForm, 
    session: AsyncSession = Depends(get_session)
):
    """
    Обновление пользователя
    """
    log.debug(f'Debug --- worker_update_by_id user.name={user.name}')
    data = user.dict()
    user = await CRUDWorker.worker_update_by_id(session, id, data)
    # log.debug(f'Debug --- worker_update_by_id session, id, data= {session} {id} {data}')
    return user

@router.delete("/{id}", response_model=bool)
async def worker_delete_by_id(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Удаление пользователя по ID
    """
    success = await CRUDWorker.worker_delete_by_id(session, id)
    return success