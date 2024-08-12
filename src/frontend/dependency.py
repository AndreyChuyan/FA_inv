from fastapi import HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from starlette.requests import Request

from worker.dependency import get_correct_worker_frontend
from database.models import Worker
from exception import RedirectException


# переход на страницу сотрудника или редирект на страницу авторизации
async def get_worker_or_redirect(
    request: Request, worker: Worker | None = Depends(get_correct_worker_frontend)
) -> Worker:
    if not worker:
        raise RedirectException(url="/auth")
    return worker


# async def get_all_workers(
#     request: Request, worker: Worker | None = Depends(get_all_workers)
# ) -> Worker:
#     if not worker:
#         raise RedirectException(url="/")
#     return worker