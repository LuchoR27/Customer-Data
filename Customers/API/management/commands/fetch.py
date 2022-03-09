from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from API.db_connector import MongoDB_Connector


class Command(BaseCommand):
    help = 'Fetch data from customers'

    def add_arguments(self, parser):
        parser.add_argument('--filepath')

    def handle(self, *args, **options):
        db_connector = MongoDB_Connector()
        path = None

        if options['filepath'] is not None:
            path = options['filepath']

        db_connector.fetch(path)
