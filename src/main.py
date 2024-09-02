from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import HTTPException, Request
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from database.database import create_tables
from objects.worker.router import router as worker_router
from frontend.router import router as frontend_router
from objects.arm.router import router as arm_router
from exception import RedirectException
from config import SECRET_KEY
# from exception import DuplicateObjectException
# from fastapi.exceptions import RequestValidationError
from prometheus_fastapi_instrumentator import Instrumentator


# отладка
import logging
def configure_logging():
    # Получить логгер Uvicorn
    log = logging.getLogger("uvicorn")
    # Удалить все существующие обработчики (handlers)
    while log.handlers:
        log.removeHandler(log.handlers[0])
    # Настроить формат логов
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    # Создать консольный обработчик и добавить форматтер
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    # Добавить обработчик к логгеру
    log.addHandler(console_handler)
    # Установить уровень логирования
    log.setLevel(logging.DEBUG)

configure_logging()
log = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info(f'Приложение запущено')
    # await create_tables()
    yield
    log.info(f'Приложение остановлено')


app = FastAPI(lifespan=lifespan)

load_dotenv()  # Загружает переменные окружения из .env файла
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
# app.add_middleware(SessionMiddleware, secret_key="secret_secret_key")

# app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")




app.include_router(worker_router)
app.include_router(frontend_router)
app.include_router(arm_router)
# app.include_router(inventory_router)


# обработка исключений с перенаправлением на url
@app.exception_handler(RedirectException)
async def redirect_exception_handler(request: Request, exc: RedirectException):
    return RedirectResponse(url=exc.headers["Location"])

# общий обработчик исключений
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# Инициализация и активация Instrumentator для сборки метрик
Instrumentator().instrument(app).expose(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", 
                host="0.0.0.0", 
                port=8000, 
                workers=2, 
                timeout_keep_alive=600,
                log_level="critical",  #    log_level="info", - для всех логов
                access_log=True, 
                use_colors=True, 
                reload=True)
