from fastapi import APIRouter, Request, Depends, status, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from objects.worker.dependency import get_correct_worker_frontend, get_current_worker
from objects.worker.crud import CRUDWorker
from objects.arm.crud import CRUDArm

from database.crud_base import Exporter
from database.models import Worker
from database.database import get_session
from .dependency import get_worker_or_redirect

import subprocess
import traceback

from prometheus_client import Counter, Summary, Histogram
import time

# отладка
import logging
log = logging.getLogger("uvicorn")

router = APIRouter(prefix="", tags=["frontend"])

templates = Jinja2Templates(directory="frontend/template")

# prometheus
REQUESTS_AUTH = Counter('get_auth_requests_total', 'Get Auth requested')
REQUESTS_AUTH_ERROR = Counter('get_auth_requests_error_total', 'Get Auth requested')
REQUESTS_LOGOUT = Counter('get_logout_requests_total', 'Get Logout requested')
REQUESTS_REGISTER = Counter('get_register_requests_total', 'Get Register requested')
REQUESTS_WORKERS = Counter('get_workers_requests_total', 'Get Workers requested')
REQUESTS_ARMS = Counter('get_arms_requests_total', 'Get Arms requested')
# Гистограмма для измерения времени обработки
REQUEST_PROCESSING_TIME = Histogram("request_processing_time_seconds", "Processing time for requests")

@router.get("/")
async def get_auth(
    request: Request, 
    worker: Worker | None = Depends(get_correct_worker_frontend)
):
    start_time = time.time()  # Начальное время (если вы не хотите использовать гистограмму как декоратор)
    if worker:
        # log.debug(f"Debug --- get_correct_worker_frontend worker.name= {worker.name}")
        REQUESTS_AUTH.inc()
        response = templates.TemplateResponse("index.html", {"request": request, "worker": worker})
    else:
        response = RedirectResponse(url="/auth", status_code=status.HTTP_301_MOVED_PERMANENTLY)
    # время задержки ответа
    REQUEST_PROCESSING_TIME.observe(time.time() - start_time)
    return response 


@router.get("/auth")
async def get_fio(
    request: Request,
    user: Worker | None = Depends(get_correct_worker_frontend),
    not_auth: bool | None = None,
):
    #  если пользователь (user) присутствует (не равен None), возвращается перенаправление (RedirectResponse) на страницу по адресу "/"
    if user:
        return RedirectResponse(url="/", status_code=status.HTTP_301_MOVED_PERMANENTLY)
    # в противном случае обрабатывается шаблон "auth.html" с передачей объекта запроса request и значения not_auth в качестве контекста (context) для шаблона
    if not_auth == True:
        REQUESTS_AUTH_ERROR.inc()
    return templates.TemplateResponse(
        "auth.html", {"request": request, "not_auth": not_auth}
    )


@router.get("/logout", response_class=RedirectResponse)
async def get_logout():
    # Создает объект RedirectResponse, который перенаправляет пользователя на главную страницу сайта (url="/").
    REQUESTS_LOGOUT.inc()
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response


# отображения страницы регистрации пользователей на сайте в зависимости от их авторизации
@router.get("/register")
async def get_register(
    request: Request, user: Worker | None = Depends(get_correct_worker_frontend)
):
    return templates.TemplateResponse("register.html", {"request": request})


# вывод данных в шаблон пользователя
@router.get("/workers")
async def get_workers(
    request: Request,
    worker: Worker = Depends(get_worker_or_redirect),
    session: AsyncSession = Depends(get_session),
):
    REQUESTS_WORKERS.inc()
    data = await CRUDWorker.get_all_worker_sorted(session)

    return templates.TemplateResponse(
        "workers/index.html",
        {"request": request, "worker": worker, "data": data},
    )
    
@router.get("/arms")
async def get_arms(
    request: Request,
    worker: Worker = Depends(get_worker_or_redirect),
    session: AsyncSession = Depends(get_session),
):
    REQUESTS_ARMS.inc()
    data = await CRUDArm.get_all_arm_sorted(session)
    data_worker = await CRUDWorker.get_all(session)
    # data_arm_user = await CRUDWorker.get_all_arm_user(session)
    return templates.TemplateResponse(
        "arms/index.html",
        {"request": request, "worker": worker, "data": data, "data_worker": data_worker},
    )

@router.get("/workers_admin")
async def get_workers(
    request: Request,
    worker: Worker = Depends(get_worker_or_redirect),
    session: AsyncSession = Depends(get_session),
):
    REQUESTS_WORKERS.inc()
    data = await CRUDWorker.get_all_worker_sorted(session)
    return templates.TemplateResponse(
        "workers_admin/index.html",
        {"request": request, "worker": worker, "data": data},
    )

@router.get("/arms_admin")
async def get_arms(
    request: Request,
    worker: Worker = Depends(get_worker_or_redirect),
    session: AsyncSession = Depends(get_session),
):
    REQUESTS_ARMS.inc()
    data = await CRUDArm.get_all_arm_sorted(session)
    data_worker = await CRUDWorker.get_all(session)
    return templates.TemplateResponse(
        "arms_admin/index.html",
        {"request": request, "worker": worker, "data": data, "data_worker": data_worker}
    )

@router.get("/workers_guest")
async def get_workers(
    request: Request,
    worker: Worker = Depends(get_worker_or_redirect),
    session: AsyncSession = Depends(get_session),
):
    REQUESTS_WORKERS.inc()
    data = await CRUDWorker.get_all_worker_sorted(session)
    return templates.TemplateResponse(
        "guest/workers.html",
        {"request": request, "worker": worker, "data": data},
    )

@router.get("/arms_guest")
async def get_arms(
    request: Request,
    worker: Worker = Depends(get_worker_or_redirect),
    session: AsyncSession = Depends(get_session),
):
    REQUESTS_ARMS.inc()
    data = await CRUDArm.get_all_arm_sorted(session)
    data_worker = await CRUDWorker.get_all(session)
    return templates.TemplateResponse(
        "guest/arms.html",
        {"request": request, "worker": worker, "data": data, "data_worker": data_worker},
    )


@router.get("/base_export_script")
async def base_export_script(
    session: AsyncSession = Depends(get_session),
):
    data = await Exporter.export_sqlite_to_excel(session)
    # log.debug(f"Debug --- base_export_script data= {data}")
    if "Export_true" in data:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="File created successfully.")
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=data)


