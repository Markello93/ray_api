# REST API
## Описание
Тестовое задание для  компании Reactive Phone
## Установка


```
git clone https://github.com/Markello93/ray_api.git
```

```bash
#### Переменные окружения
Для работы приложения необходимы следующие переменные окружения
(создать файл `.env` в корневой директории проекта)
# Общие настройки контейнера приложения
DB_NAME=postgres    # имя базы данных
DB_USER=postgres    # имя пользователя базы данных
DB_PASS=postgres   # пароль для базы данных
DB_HOST=localhost / postgres   # имя хоста (контейнера) базы данных
DB_PORT=5432       # порт, на котором работает база данных
# Настройки контейнера базы данных
POSTGRES_USER=postgres      # имя суперпользователя postgres
POSTGRES_PASSWORD=postgres  # пароль суперпользователя
# Настройки для подключения Redis
REDIS_HOST=localhost / redis                         # название тестовой БД redis
REDIS_PORT=6379                         # порт, на котором работает Бд
```
#### Запуск проекта:
1) установка зависимостей через pip
```
pip install requirements.txt
```
или через poetry:

```
poetry install
```

2) Запуск проекта
```
python manage.py runserver
```

3) Запуск тестов:
```
python manage.py test
```

# Документация

Доступ к документации представлен по ссылке


[http://127.0.0.1:8000/api/docs](http://127.0.0.1:8000/api/docs)
