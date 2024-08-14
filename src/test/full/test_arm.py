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
from arm.schemas import ArmBase

client = TestClient(app)

@pytest.fixture(scope="session")
def sample() -> Arm:
    return Arm(
        title="Test title",
        department_arm="2",
        location="Test Location",
        name="Test Arm",
        model="Test Model",
        release="Test release",
        num_serial="Test num_serial",
        num_invent="Test num_invent",
        num_service="Test num_service",
        price="Test price",
        formular="Test formular",
        state="Test state",
        description="Test Description",
        description2="Test Description2",
        description3="Test Description3"
    )

def test_create_arm(sample: Arm):
    sample_arm = {
        "title": sample.title,
        "department_arm": sample.department_arm,
        "location": sample.location,
        "name": sample.name,
        "model": sample.model,
        "release": sample.release,
        "num_serial": sample.num_serial,
        "num_invent": sample.num_invent,
        "num_service": sample.num_service,
        "price": sample.price,
        "formular": sample.formular,
        "state": sample.state,
        "description": sample.description,
        "description2": sample.description2,
        "description3": sample.description3
    }
    response = client.post("/arm/", json=sample_arm)
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
    assert response.json()["title"] == sample.title
    assert response.json()["department_arm"] == sample.department_arm
    
# def test_get_all_arm(sample):
#     sample_arm = sample
#     response = client.get("/arm/")
#     assert response.status_code == 200
#     assert len(response.json()) > 0
#     # Проверяем формат данных пользователей
#     for arm in response.json():
#         assert "title" in arm
#         assert "department_arm" in arm
    # Проверяем, что данные объекта Arm присутствуют в полученном списке
    # assert any(obj['title'] == sample_arm.title for obj in response.json())
    # assert any(obj['department_arm'] == sample_arm.department_arm for obj in response.json())



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