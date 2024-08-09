from pydantic import BaseModel
from typing import Optional
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"

class WorkerBase(BaseModel):
    name: str
    role: str
    password: str
    deparment: str
    description: str

class WorkerCreate(WorkerBase):
    password: str

class WorkerOut(WorkerBase):
    id: int
    role: str
    name: str
