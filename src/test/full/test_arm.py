# import sys
# sys.path.append(r'C:\Users\legion\projects\NEW\investment_portfolio\src')
import os
import sys
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))  # Получаем абсолютный путь к директории src
sys.path.append(src_dir)  # Добавляем путь к директории src в список путей для импорта модулей
# print(src_dir)

import pytest
# from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient
from database.models import Arm
from main import app

client = TestClient(app)


data = {
    "name": "Test Arm",
    "department_arm": "Test Department",
    "location": "Test Location",
    "model": "Test Model",
    "serial": "Test Serial",
    "inventarial": "Test Inventarial",
    "description": "Test Description"
}

def test_get_all_arm():
    response = client.get("/arm/")
    assert response.status_code == 200  # 200 OK
    response_data = response.json()
    # Проверяем, что полученные данные являются списком объектов ArmOut
    assert isinstance(response_data, list)
    for item in response_data:
        assert "name" in item
        assert "department_arm" in item
    

def test_create():
    resp = client.post("/arm/", json=data)
    response_data = resp.json()
    assert resp.status_code == 201  # Проверяем, что объект был успешно создан (201 Created)
    assert response_data["name"] == data["name"]
    assert response_data["department_arm"] == data["department_arm"]
    
    
# def test_create_duplicate(sample):
#     resp = client.post("/arm", json=sample.dict())
#     assert resp.status_code == 404

# def test_get_one(sample):
#     resp = client.get(f"/arm/{sample.name}")
#     assert resp.json() == sample.dict()

# def test_get_one_missing():
#     resp = client.get("/arm/bobcat")
#     assert resp.status_code == 404

# def test_modify(sample):
#     resp = client.patch(f"/arm/?name={sample.name}", json=sample.dict())
#     assert resp.json() == sample.dict()

# def test_modify_missing(sample):
#     resp = client.patch("/arm/?name=rougarou", json=sample.dict())
#     assert resp.status_code == 404

# def test_delete(sample):
#     resp = client.delete(f"/arm/{sample.name}")
#     assert resp.status_code == 200
#     assert resp.json() is True

# def test_delete_missing(sample):
#     resp = client.delete(f"/arm/{sample.name}")
#     assert resp.status_code == 404