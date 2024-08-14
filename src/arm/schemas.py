from pydantic import BaseModel
from typing import Optional
from enum import Enum


class ArmBase(BaseModel):
    title: str
    department_arm: str
    location: str
    name: str
    model: str
    release: str
    num_serial: str
    num_invent: str
    num_service: str
    price: str
    formular: str
    state: str
    description: str
    description2: str
    description3: str

class ArmOut(ArmBase):
    id: int
    title: str
    num_serial: str

class ArmForm(BaseModel):
    title: str
    location: str
    name: str
    model: str
    release: str
    num_serial: str
    num_invent: str
    num_service: str
    price: str
    formular: str
    state: str
    description: str
    description2: str
    description3: str