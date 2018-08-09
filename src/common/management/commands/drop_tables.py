from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Drop all tables"

    def handle(self, *args, **options):
        cursor = connection.cursor()

        tables = connection.introspection.table_names()

        for table in tables:
            print('Droping table %s...' % table)
            cursor.execute('DROP TABLE IF EXISTS "%s" CASCADE;' % table)