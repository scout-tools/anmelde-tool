from django.core.management.base import BaseCommand
import glob, os
from django.core.management import call_command


class Command(BaseCommand):
    help = 'add all fixtures'

    def add_arguments(self, parser):
        parser.add_argument('directory', nargs='+', type=str)

    def handle(self, *args, **options):
        for dir in options['directory']:
            files = glob.glob(os.path.join(dir, '*.json'))
            print(files)
            for file in files:
                print(file)
                call_command('loaddata', file)
