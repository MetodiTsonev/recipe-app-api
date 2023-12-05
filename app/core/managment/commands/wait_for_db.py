"""
Command to wait for the database to be available
"""
import time

from psycopg2 import OperationalError as Psycopg2Error

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('waiting for database ...')
        db_up = False
        while not db_up:
            try:
                # This will raise an exception if the connection fails
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second ...')
                time.sleep(1)

            self.stdout.write(self.style.SUCCESS('Database available!'))