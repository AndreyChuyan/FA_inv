from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Float,
    DateTime,
    Enum,
    Boolean,
)
from sqlalchemy.orm import declarative_base, relationship
import enum
from sqlalchemy import Sequence

from database.database import Base


class Role(enum.Enum):
    admin = "admin"
    user = "user"
    guest = "guest"


class Worker(Base):
    __tablename__ = "worker"
    id = Column(Integer, primary_key=True)
    role = Column(Enum(Role), default=Role.guest)
    fio = Column(String)
    name = Column(String, unique=True)
    password = Column(String)
    department = Column(String)
    position = Column(String)
    description = Column(String, default=None)

    conn_worker_arm = relationship(
        "Arm", back_populates="conn_arm_worker"
    )

    def as_dict(self):
        return {
            "id": self.id,
            "role": self.role.name,  # предполагая, что Enum имеет атрибут `name`
            "fio": self.fio,
            "name": self.name,
            "password": self.password,
            "department": self.department,
            "position": self.position,
            "description": self.description
        }
    # def __str__(self):
    #     return f"Worker: {self.name} Role: {self.role} ID: {self.id}"


class Arm(Base):
    __tablename__ = "arm"
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    department_arm = Column(String)
    location = Column(String)
    name = Column(String)
    model = Column(String)
    release = Column(String)
    num_serial = Column(String)
    num_invent = Column(String)
    num_service = Column(String)
    price = Column(String)
    formular = Column(String)
    state = Column(String)
    description = Column(String, default=None)
    description2 = Column(String, default=None)
    description3 = Column(String, default=None)
    id_worker = Column(Integer, ForeignKey("worker.id"), default=1)
    
    conn_arm_worker = relationship(
        "Worker", back_populates="conn_worker_arm"
    )

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "department_arm": self.department_arm,
            "location": self.location,
            "name": self.name,
            "model": self.model,
            "release": self.release,
            "num_serial": self.num_serial,
            "num_invent": self.num_invent,
            "num_service": self.num_service,
            "price": self.price,
            "formular": self.formular,
            "state": self.state,
            "description": self.description,
            "description2": self.description2,
            "description3": self.description3,
            "id_worker": self.id_worker
        }