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
    login = Column(String)
    name = Column(String)
    password = Column(String)
    department = Column(String)
    position = Column(String)
    description = Column(String, default=None)

    conn_worker_arm = relationship(
        "Arm", back_populates="conn_arm_worker"
    )

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

    # def __str__(self):
    #     return f"Arm: {self.name} department: {self.department} ID: {self.id}"


# class Inventory(Base):
#     __tablename__ = "inventory"
#     id = Column(Integer, primary_key=True)
#     id_worker = Column(Integer, ForeignKey("worker.id"), default=1)
#     id_arm = Column(Integer, ForeignKey("arm.id"), default=1)

#     conn_inventory_worker = relationship(
#         "Worker", back_populates="conn_worker_inventory"
#     )
#     conn_inventory_arm = relationship(
#         "Arm", back_populates="conn_arm_inventory"
#         )
