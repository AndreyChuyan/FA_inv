﻿from pydantic import BaseModel
from typing import Optional
from enum import Enum


class Role(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"


class WorkerBase(BaseModel):
    role: str
    login: str
    name: str
    password: str
    department: str
    position: str
    description: str


class WorkerCreate(WorkerBase):
    password: str


class WorkerOut(WorkerBase):
    id: int
    role: str
    name: str
