from fastapi import APIRouter, HTTPException
from .model import Worker
from worker import service as service
from error import Duplicate, Missing

router = APIRouter(prefix="/worker")

# --- CRUD
# @router.get("")
@router.get("/")
def get_all() -> list[Worker]:
    return service.get_all()

@router.get("/{name}")
def get_one(name) -> Worker | None:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.post("/", status_code=201)
def create(worker: Worker) -> Worker:
    try:
        return service.create(worker)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
        
@router.patch("/")
def modify(name: str, worker: Worker) -> Worker:
    try:
        return service.modify(name, worker)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
        
@router.delete("/{name}")
def delete(name: str):
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)