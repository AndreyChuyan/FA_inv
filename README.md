# FA_inv

## start
python -m venv .venv
.\.venv\Scripts\activate

pip install -r requirements.txt
### запись зависимостей
pip freeze > requirements.txt

<!-- uvicorn src.main:app --reload -->
cd .\src\
python main.py


http://127.0.0.1:8000/docs

### форматирование
black .\src\*

set PYTHONPATH=C:\Users\Noteburg\git\FA_inventory\src

### отладка 
$path = 'user/'; (Invoke-WebRequest -Uri http://localhost:8000/$path).Content
$path = 'user'; (Invoke-WebRequest -Uri http://localhost:8000/$path).Content

<!-- для CSS - загрузить локально -->
https://www.cleancss.com/css-beautify/3

<!-- Удалить локальные изменения -->
git add .
git commit -m "Сообщение коммита"
git clean -f
git fetch origin main
git reset --hard origin/main


- определить в описании тип компьютера
- сделать страницу для пользователя с просмотром компьютеров и минимальной инфой
- функция вывода базы данных в excel в указанную директорию
- релиз!