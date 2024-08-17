from contextlib import asynccontextmanager

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
# from objects.inventory.router import router as inventory_router
from exception import RedirectException
from config import SECRET_KEY
from exception import DuplicateObjectException
from fastapi.exceptions import RequestValidationError

# отладка
import logging
log = logging.getLogger("uvicorn")
log.setLevel(logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается...")
    # await create_tables()
    yield
    print("Приложение останавливается...")


app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")





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




if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
