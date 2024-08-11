from pydantic import BaseModel


class Arm(BaseModel):
    name: str
    number: str
    department: str
    description: str
