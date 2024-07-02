from django.core.management.base import BaseCommand
from dashboard.models import Task

class Command(BaseCommand):
    """Your logic to update the task status"""
    help = 'Update task statuses'

    def handle(self, *args, **kwargs):
        tasks = Task.objects.all()
        for task in tasks:
            if task.start_date <= task.due_date:
                task.save()
                self.stdout.write(self.style.SUCCESS('Successfully updated task statuses'))
            else:
                self.stdout.write(self.style.ERROR(f'Task {task.task_id} has invalid dates.'))