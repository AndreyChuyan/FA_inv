from .model import Worker
import data.worker as data

# --- CRUD
def get_all() -> list[Worker]:
    return data.get_all()

def get_one(name: str) -> Worker | None:
    return data.get_one(name)

def create(worker: Worker) -> Worker:
    return data.create(worker)

def modify(name, worker: Worker) -> Worker:
    return data.modify(name, worker)

def delete(name: str) -> bool:
    return data.delete(name)