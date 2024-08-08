from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from arm import arm

# from data.database import create_tables
# from user.router import router as user_router
# from frontend.router import router as frontend_router
# from exception import RedirectException


# асинхронный контекстный менеджер, который используется для управления жизненным циклом вашего приложения
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается...")
    # Вызывает функцию create_tables() асинхронно для создания таблиц
    # await create_tables()
    yield
    print("Приложение останавливается...")


# Создает экземпляр FastAPI с использованием параметра lifespan, который является определенным контекстным менеджером для управления жизненным циклом приложения.
app = FastAPI(lifespan=lifespan)
# Добавляет Middleware к приложению FastAPI, в данном случае SessionMiddleware с заданным секретным ключом
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# Монтирует статические файлы из директории "frontend/assets" на путь "/assets" в вашем приложении.
# app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")

# Включает маршрутизаторы (routers)
# app.include_router(worker.router)
app.include_router(arm.router)


# Регистрирует обработчик исключений для пользовательского исключения RedirectException.
#    - В случае возникновения этого исключения, обработчик будет возвращать RedirectResponse, перенаправляя клиента по указанному URL.
# @app.exception_handler(RedirectException)
# async def redirect_exception_handler(request: Request, exc: RedirectException):
#     return RedirectResponse(url=exc.headers["Location"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
