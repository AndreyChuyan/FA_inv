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
    name = Column(String)
    role = Column(Enum(Role), default=Role.guest)
    password = Column(String)
    deparment = Column(String)
    description = Column(String, default=None)

    conn_worker_inventory = relationship(
        "Inventory", back_populates="conn_inventory_worker"
    )

    def __str__(self):
        return f"Worker: {self.name} Email: {self.role} ID: {self.id}"


class Arm(Base):
    __tablename__ = "arm"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    deparment = Column(String)
    description = Column(String, default=None)

    conn_arm_inventory = relationship("Inventory", back_populates="conn_inventory_arm")

    def __str__(self):
        return f"Arm: {self.name} Email: {self.deparment} ID: {self.id}"


class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True)
    id_worker = Column(Integer, ForeignKey("worker.id"), default=1)
    id_arm = Column(Integer, ForeignKey("arm.id"), default=1)

    conn_inventory_worker = relationship(
        "Worker", back_populates="conn_worker_inventory"
    )
    conn_inventory_arm = relationship("Arm", back_populates="conn_arm_inventory")
