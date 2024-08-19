from fastapi import APIRouter, Request, Depends, status, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from objects.worker.dependency import get_correct_worker_frontend, get_current_worker
from objects.worker.crud import CRUDWorker
from objects.arm.crud import CRUDArm

# from database.crud_base import CRUDBase
from database.models import Worker
from database.database import get_session
from .dependency import get_worker_or_redirect



# отладка
import logging
log = logging.getLogger("uvicorn")

router = APIRouter(prefix="", tags=["frontend"])

templates = Jinja2Templates(directory="frontend/template")


@router.get("/")
async def get_auth(
    request: Request, 
    worker: Worker | None = Depends(get_correct_worker_frontend)
):
    if worker:
        log.debug(f"Debug --- get_correct_worker_frontend worker.name= {worker.name}")
        return templates.TemplateResponse("index.html", {"request": request, "worker": worker})
    else:
        return RedirectResponse(url="/auth", status_code=status.HTTP_301_MOVED_PERMANENTLY)


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
    return templates.TemplateResponse(
        "auth.html", {"request": request, "not_auth": not_auth}
    )


@router.get("/logout", response_class=RedirectResponse)
async def get_logout():
    # Создает объект RedirectResponse, который перенаправляет пользователя на главную страницу сайта (url="/").
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
    data = await CRUDWorker.get_all_worker_sorted(session)
    # log.debug(f"Debug --- /workers data_users= {data_users}")
    # log.debug(f"Debug --- /workers data_users[0][0].name= {data_users[0][0].name}")
    # data = [{"id": i, **dct} for i, dct in enumerate(data, start=1)]
    # print(data)
    # workers = await CRUDWorker.get_all(session)
    # arms = await CRUDArm.get_all(session)
    # # disciplines = await CRUDDiscipline.get_all(session)

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
    data = await CRUDArm.get_all_arm_sorted(session)
    data_worker = await CRUDWorker.get_all(session)

    log.debug(f"Debug --- /arms data= {data}")
    log.debug(f"Debug --- /arms data_users= {data_worker}")
    log.debug(f"Debug --- /arms data_users[0].name= {data_worker[0].name}")
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
    data = await CRUDWorker.get_all_worker_sorted(session)
    return templates.TemplateResponse(
        "workers_admin/index.html",
        {"request": request, "worker": worker, "data": data},
    )



