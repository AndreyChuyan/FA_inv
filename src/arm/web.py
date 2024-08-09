from fastapi import APIRouter, HTTPException
from .model import Arm
from arm import service as service
from error import Duplicate, Missing

router = APIRouter(prefix="/arm")


# @router.get("")
@router.get("/")
def get_all() -> list[Arm]:
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> Arm | None:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("/")
def create(arm: Arm) -> Arm:
    try:
        return service.create(arm)
    except Duplicate as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.patch("/")
def modify(name: str, arm: Arm) -> Arm:
    try:
        return service.modify(name, arm)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("/{name}")
def delete(name: str):
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
