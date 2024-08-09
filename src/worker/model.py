from pydantic import BaseModel
from typing import Optional

class Worker(BaseModel):
    name: str
    role: str
    password: str
    deparment: str
    description: str
