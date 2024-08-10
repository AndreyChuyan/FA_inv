from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.requests import Request

from database.database import get_session
from .auth import verify_token, verify_token_not_exception
from .crud import CRUDWorker
from .exceptions import exception_user_not_found, exception_auth


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/worker/token",
    auto_error=False,
)


async def get_current_worker(
    token: str | None = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
):
    if not token:
        raise exception_auth
    username = verify_token(token, exception_auth)
    user = await CRUDWorker.get_worker_by_name(session, username)
    if user is None:
        raise exception_user_not_found
    return user


# принимает объект запроса Request и извлекает из него значение токена доступа (access_token) из куки (cookie).
async def get_token_cookie(request: Request):
    return request.cookies.get("access_token")


# используется для получения данных о рабочем сотруднике (worker) на фронтенде (frontend).
# Функция принимает токен доступа (token) в качестве параметра, а также сессию базы данных (AsyncSession) в качестве зависимости
async def get_correct_worker_frontend(
    token: str | None = Depends(get_token_cookie),
    session: AsyncSession = Depends(get_session),
):
    if token:
        # вернем имя пользователя через токен
        username = verify_token_not_exception(token)
        if username:
            user = await CRUDWorker.get_worker_by_name(session, username)
            return user


async def get_worker_by_id(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await CRUDWorker.get_by_id(session, user_id)
    if user is None:
        raise exception_user_not_found
    return user
