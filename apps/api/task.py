import aiohttp
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.posts.models import PexelsImage
from config import settings

User = get_user_model()


# @shared_task
# def send_otp_to_user_email(email, otp_code):
#     subject = "Your OTP password"
#     confirmation_url = reverse("token_obtain_pair")
#     full_confirmation_url = f"http://logevityapi.hopto.org{confirmation_url}"
#     message = f"""
#     <html>
#     <body>
#         <p>Your OTP password: {otp_code}</p>
#         <p>Confirm OTP <a href="{full_confirmation_url}">here</a>.</p>
#     </body>
#     </html>
#     """
#
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#
#     send_mail(subject, "", from_email, recipient_list, html_message=message)


# app/tasks.py

import os
from celery import shared_task
from django.conf import settings
from datetime import datetime


# @shared_task
# def create_database_backup():
#     # Получаем имя базы данных
#     db_name = settings.DATABASES['default']['NAME']
#
#     # Создаем имя файла бэкапа с учетом времени выполнения
#     backup_filename = f"{db_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql"
#
#     # Команда для создания бэкапа базы данных
#     backup_command = f"pg_dump {db_name} > {backup_filename}"  # Предполагается, что вы используете PostgreSQL
#
#     os.system(backup_command)


@shared_task
def create_database_backup():
    db_name = settings.DATABASES['default']['NAME']
    backup_filename = f"{db_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"

    # Команда для создания бэкапа базы данных SQLite в формате JSON
    backup_command = f"sqlite3 {db_name} '.dump' > {backup_filename}"

    os.system(backup_command)

# @shared_task
# async def fetch_pexels_images():
#     url = 'https://api.pexels.com/v1/search?query=cars&per_page=5'
#     headers = {
#         'Authorization': 'Bearer YOUR_API_KEY_HERE'
#     }
#
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, headers=headers) as response:
#             if response.status == 200:
#                 data = await response.json()
#                 photos = data.get('photos', [])
#                 for photo in photos:
#                     image_data = {
#                         'url': photo.get('url'),
#                         'description': photo.get('alt'),
#                         'photographer': photo.get('photographer')
#                     }
#                     # Создание объекта модели и сохранение в БД
#                     pexels_image = PexelsImage.objects.create(**image_data)
#                     pexels_image.save()
#             else:
#                 print(f"Failed to fetch images. Status code: {response.status}")
#postgresql
@shared_task
def create_database_backup():
    db_name = settings.DATABASES['default']['NAME']
    backup_filename = f"{db_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"

    # Команда для создания бэкапа базы данных PostgreSQL в формате JSON
    backup_command = f"pg_dump --format=json {db_name} > {backup_filename}"

    os.system(backup_command)