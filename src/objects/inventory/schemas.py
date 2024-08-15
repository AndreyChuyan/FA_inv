from pydantic import BaseModel
from typing import Optional
from enum import Enum


class InventoryBase(BaseModel):
    id_worker: int
    id_arm: int

class InventoryOut(InventoryBase):
    id_worker: int
    id_arm: int
    
class InventoryForm(InventoryBase):
    id_worker: int
    id_arm: int