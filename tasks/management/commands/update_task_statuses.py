from django.core.management.base import BaseCommand
from dashboard.models import Task

class Command(BaseCommand):
    help = 'Update task statuses based on defined rules'
    
    def handle(self, *args, **kwargs):
        tasks = Task.objects.all()
        for task in tasks:
            task.update_status()
        self.stdout.write(self.style.SUCCESS('Successfully updated task statuses'))
