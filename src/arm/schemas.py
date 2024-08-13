from pydantic import BaseModel
from typing import Optional
from enum import Enum


class ArmBase(BaseModel):
    name: str
    department: str
    location: str
    model: str
    serial: str
    inventarial: str
    description: str


class ArmOut(ArmBase):
    id: int
    name: str
    serial: str

class ArmForm(BaseModel):
    name: str
    location: str
    model: str
    serial: str
    inventarial: str
    description: str