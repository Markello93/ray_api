from celery import shared_task
from django.core import management


@shared_task
def create_database_backup():
    """ Task to perform a database backup."""
    management.call_command('dbbackup')
