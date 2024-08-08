from .model import Arm
from .data import arm as data

def get_all() -> list[Arm]:
    return data.get_all()

def get_one(name: str) -> Arm | None:
    return data.get_one(name)

def create(arm: Arm) -> Arm:
    return data.create(arm)

# def replace(id, arm: Arm) -> Arm:
#     return data.replace(id, arm)

def modify(name, arm: Arm) -> Arm:
    return data.modify(name, arm)

def delete(name) -> bool:
    return data.delete(name)