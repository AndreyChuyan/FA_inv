# Инвентарный учет
# Автор - Чуян Андрей

Приложение предназначено для организованного сбора, группировки и представления сводных данных об используемой в организации компьютерной технике и пользователях, закреплённых за ней. Оно включает систему аутентификации и разграничения доступа к ресурсам в зависимости от роли (администратор, ответственный, пользователь).
- Роль администратора: создание и редактирование всех объектов, назначение ролей, сохранение базы в формате xlsx (Microsoft Excel).
- Роль ответственного: создание и редактирование сведений о пользователях и компьютерах своего подразделения, без возможности назначения ролей.
- Роль пользователя: просмотр ограниченных сведений о пользователях и компьютерах в подразделении.

## Функционал

### Аутентификация

![Alt текст](.md/1.jpg)

### Роль администратора
#### Создание и редактирование пользователей приложения
![Alt текст](.md/2.jpg)
пользователи
![Alt текст](.md/2_2.jpg)
компьютеры
![Alt текст](.md/3.jpg)

#### Экспорт базы данных в Exel
![Alt текст](.md/4.jpg)
![Alt текст](.md/5.jpg)

### Кабинет ответственного за учет
![Alt текст](.md/6.jpg)
#### Создание и редактирование пользователей подразделения
![Alt текст](.md/7.jpg)
#### Создание и редактирование компьютерной техники подразделения
![Alt текст](.md/8.jpg)


### Кабанет пользователя
![Alt текст](.md/9.jpg)
![Alt текст](.md/10.jpg)
![Alt текст](.md/11.jpg)

## Запуск в консольном режиме

```bash
# Подготовка
# в директории main создайте файл окружения .env с содержимым секретного ключа для генерации токена
echo "" > ./src/.env
SECRET_KEY=<значение секретного ключа>

mkdir db
mkdir export
# запуск
# Windows
# Напрямую с интерпретатора
# создание окружения
python -m venv .venv
# переход в окружение 
source .venv/bin/activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
# pip freeze > requirements.txt # для записей завиимостей 
# deactivate # выход из виртуального окружения

# запуск
cd .\src\
python main.py

#Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd .\src\
python main.py


# Контейнер Docker
docker build -t app-inventory .
docker run -d -p 80:8000 app-inventory 

    ## для удаления
    docker stop app-inventory 
    docker rm -f app-inventory

# Docker-Compose
docker-compose up
    # запуск в фоне
    docker-compose up -d
    # удаление
    docker-compose down

```

# Просмотр логов
sudo tail -f /var/log/python_app_inventory.log


# Promethus метрики
## Graphana дашборды 
![Alt текст](.md/12.jpg)

дашборд доступен по FA_inv/Инвентарный учет-1725356679506.json

## Метрики
```bash
get_auth_requests_total         # число реквестов главной страницы
get_auth_requests_error_total   # число реквестов ошибок авторизации
get_logout_requests_total       # число реквестов выхода из приложения
get_workers_requests_total      # число запросов к пользователям
get_arms_requests_total         # число запросов к армам

worker_create_total             # число созданных пользователей
arm_create_total                # число созданных пользователей

rate(get_auth_requests_total{}[20m])             # Частота запросов в течение 5 минут
rate(get_auth_requests_error_total{}[20m])       # Частота ошибок авторизации
rate(worker_create_total{}[20m])                 # Частота создания пользователей
rate(arm_create_total{}[20m])                    # Частота создания армов

sum(rate(request_processing_time_seconds_sum[5m])) / sum(rate(request_processing_time_seconds_count[5m]))     # Средняя время обработки запроса за 5 минут



