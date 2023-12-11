# REST API
## Описание
Тестовое задание для  компании Reactive Phone

## Краткое описание функционала проекта
Проект представляет собой API блога про автомобили.
API позволяет создавать пользователям посты, комментарии и ставить лайки постам.

Так же в проекте есть endpoint на получение текста последнего поста по интересующей
пользователя теме, с добавлением связанных с темой изображений с внешнего API.

Создана фоновая задача на выполнение бэкапа БД. Фоновая задача запускается
через Celery.

## Установка


```
git clone https://github.com/Markello93/ray_api.git
```

```bash
#### Переменные окружения
Для работы приложения необходимо создать файл .env в корневой
директории проекта и задать в нём следующие переменные окружения:
# Общие настройки контейнера приложения

# Имя базы данных PostgreSQL
DB_NAME=postgres
# Имя хоста (контейнера) базы данных
DB_HOST=localhost / postgres
# Порт, на котором работает база данных
DB_PORT=5432
# Настройки контейнера базы данных
# Имя суперпользователя Postgres
POSTGRES_USER=postgres
# Пароль суперпользователя Postgres
POSTGRES_PASSWORD=postgres

#Настройки для подключения Redis

# Название БД redis
REDIS_HOST=localhost / redis
# Порт, на котором работает Бд
REDIS_PORT=6379

#Настройки проекта Django

#Установка DEBUG режима проекта, по умолчанию стоит False
DEBUG=True
#Включение логирования SQL запросов для отладки ( по умолчанию False)
LOGGING_ENABLED= True/False

```
## Запуск проекта:
### 1) Запуск проекта через поднятие контейнеров в docker:
* поднятие контейнеров
```
 docker compose up --build
```
* создание супер пользователя
```
docker compose run --rm ray_api python manage.py createsuperuser
 ```
* запуск тестов
```
docker compose run --rm ray_api python manage.py test
 ```
### 2) Запуск проекта без использования docker
* установка зависимостей через pip
```
pip install requirements.txt
```
или через poetry:

```
poetry install
```

* Применение миграций
```
python manage.py migrate
```
* Создание учетной записи админа
```
python manage.py createsuperuser
```
* Запуск проекта:
```
python manage.py runserver
```
* Запуск тестов:
```
python manage.py test
```

# Документация

Доступ к документации представлен по ссылке


[http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)
