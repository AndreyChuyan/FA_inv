# Инвентарный учет

Приложение работает на фреймворке FastAPI предназначено для организованного сбора, группировки и представления сводных данных об используемых в организации компьютерной техники и пользователях, закрепленных за ней. Имеет систему аутентификации и разделения доступа к ресурсам, в зависимости от роли (администратор, пользователь, гость).

## Функционал

### Аутентификация

![Alt текст](.md/1.jpg)

### Роль администратора
#### Создание и редактирование пользователей приложения
![Alt текст](.md/2.jpg)
кабинет администратора
![Alt текст](.md/2_2.jpg)
редактирование пользователя
![Alt текст](.md/3.jpg)

#### Экспорт базы данных в Exel
![Alt текст](.md/4.jpg)
![Alt текст](.md/5.jpg)

### Роль ответственного за учет
![Alt текст](.md/6.jpg)
#### Создание и редактирование пользователей подразделения
![Alt текст](.md/7.jpg)

#### Создание и редактирование компьютерной техники подразделения
![Alt текст](.md/8.jpg)


### Роль пользователя
![Alt текст](.md/9.jpg)
![Alt текст](.md/10.jpg)

## Запуск в консольном режиме

```bash
# Windows
# Напрямую с интерпретатора
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
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
