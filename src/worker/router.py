from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse, Response

from database.database import get_session
from database.models import Worker
from .schemas import WorkerCreate, WorkerOut
from .crud import CRUDWorker
from .dependency import get_current_worker, get_worker_by_id

from .auth import hash_password, verify_password, create_access_token
from .exceptions import exception_user_not_found, exception_auth, exception_unique_field

router = APIRouter(prefix="/worker", tags=["tag_worker"])


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
        return RedirectResponse(url="/auth?not_auth=true", status_code=status.HTTP_303_SEE_OTHER)
    access_token = create_access_token(data={"sub": user.username})
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token)
    return response


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
    return users

