from fastapi import FastAPI
import os
import sys
from typing import Optional

# --- логирование
import logging
log = logging.getLogger("uvicorn")
log.setLevel(logging.DEBUG)
# Пример использования логгера
# logger.debug('Debug message')
# logger.info('Info message')
# logger.warning('Warning message')
# logger.error('Error message')
# logger.critical('Critical message')

# Получаем текущий каталог скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))
# Добавляем путь к папке с модулем utils.py в переменную окружения PYTHONPATH
parent_dir = os.path.dirname(script_dir)
sys.path.append(parent_dir)
path_to_json = os.path.join(parent_dir, 'arm.json')
# Теперь можно импортировать модуль utils.py
from utils import json_to_dict_list

app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Привет, Хабр!"}

@app.get("/arm")
def get_all_arm(department: Optional[int] = None):
    arms = json_to_dict_list(path_to_json)
    if department is None:
        return arms
    else:
        return_list = []
        for arm in arms:
            if arm["department"] == department:
                return_list.append(arm)
        return return_list

@app.get("/arm/{department}")
def get_all_arm_department(department: int, description: Optional[str] = None):
    arms = json_to_dict_list(path_to_json)
    return_list = []
    for arm in arms:
        if arm["department"] == department:
            return_list.append(arm)
            
    if description:
        return_list = [arm for arm in return_list if arm['description'].lower() == description.lower()]
    
    return return_list