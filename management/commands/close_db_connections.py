from django.core.management.base import BaseCommand
from django.db import connections

class Command(BaseCommand):
    help = 'Closes all database connections'

    def handle(self, *args, **options):
        for conn in connections.all():
            conn.close_if_unusable_or_obsolete()
        self.stdout.write(self.style.SUCCESS('Successfully closed all database connections'))