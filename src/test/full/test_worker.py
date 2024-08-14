import pytest
from fastapi.testclient import TestClient
from model.worker import Worker
from main import app

client = TestClient(app)

@pytest.fixture(scope="session")
def sample() -> Worker:
    return Worker(name="test_name", deparment="test_dep", description="test_desc")

def test_create(sample):
    resp = client.post("/worker", json=sample.dict())
    assert resp.status_code == 201

def test_create_duplicate(sample):
    resp = client.post("/worker", json=sample.dict())
    assert resp.status_code == 404

def test_get_one(sample):
    resp = client.get(f"/worker/{sample.name}")
    assert resp.json() == sample.dict()

def test_get_one_missing():
    resp = client.get("/worker/bobcat")
    assert resp.status_code == 404

def test_modify(sample):
    resp = client.patch(f"/worker/?name={sample.name}", json=sample.dict())
    assert resp.json() == sample.dict()

def test_modify_missing(sample):
    resp = client.patch("/worker/?name=rougarou", json=sample.dict())
    assert resp.status_code == 404

def test_delete(sample):
    resp = client.delete(f"/worker/{sample.name}")
    assert resp.status_code == 200
    assert resp.json() is True

def test_delete_missing(sample):
    resp = client.delete(f"/worker/{sample.name}")
    assert resp.status_code == 404