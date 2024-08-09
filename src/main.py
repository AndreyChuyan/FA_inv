from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from database.database import create_tables
from worker.router import router as worker_router
# from frontend.router import router as frontend_router
from exception import RedirectException



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Приложение запускается...")
    await create_tables()
    yield
    print("Приложение останавливается...")


app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")

# app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")

app.include_router(worker_router)
# app.include_router(frontend_router)


@app.exception_handler(RedirectException)
async def redirect_exception_handler(request: Request, exc: RedirectException):
    return RedirectResponse(url=exc.headers["Location"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
