from pydantic import BaseModel


class Arm(BaseModel):
    name: str
    number: str
    deparment: str
    description: str
