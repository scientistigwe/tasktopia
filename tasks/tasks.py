from celery import shared_task
from dashboard.models import Task
from datetime import date

@shared_task
def update_task_statuses():
    tasks = Task.objects.all()
    for task in tasks:
        task.update_status()