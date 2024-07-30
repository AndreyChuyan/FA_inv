# FA_inv
## Создаем о туториалу
https://habr.com/ru/companies/amvera/articles/826196/ Создание собственного API на Python (FastAPI): Знакомство и первые функции
https://habr.com/ru/articles/827134/ Создание собственного API на Python (FastAPI): Гайд по POST, PUT, DELETE запросам и моделям Pydantic
https://habr.com/ru/articles/827222/ Создание собственного API на Python (FastAPI): структура проекта, SQLAlchemy PostgreSQL, миграции и первые модели таблиц
https://habr.com/ru/articles/828328/ Создание собственного API на Python (FastAPI): Router и асинхронные запросы в PostgreSQL (SQLAlchemy)
https://habr.com/ru/articles/829742/ Создание собственного API на Python (FastAPI): Авторизация, Аутентификация и роли пользователей
https://habr.com/ru/articles/831386/ Создание собственного API на Python (FastAPI): Подключаем фронтенд и статические файлы

## start
python -m venv .venv
.\.venv\Scripts\activate

pip install -r requirements.txt
### запись зависимостей
pip freeze > requirements.txt

<!-- uvicorn src.main:app --reload -->
python .\app\main.py


http://127.0.0.1:8000/docs

### форматирование
black .\src\*

set PYTHONPATH=C:\Users\Noteburg\git\FA_inventory\src

### отладка 
$path = 'user/'; (Invoke-WebRequest -Uri http://localhost:8000/$path).Content
$path = 'user'; (Invoke-WebRequest -Uri http://localhost:8000/$path).Content