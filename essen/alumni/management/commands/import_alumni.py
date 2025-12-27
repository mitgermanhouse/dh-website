import os
from django.core.management.base import BaseCommand
from alumni.utils import import_alumni_from_xlsx

class Command(BaseCommand):
    help = 'Import alumni from xlsx file using openpyxl'

    def add_arguments(self, parser):
        parser.add_argument('xlsx_file', type=str, help='Path to the xlsx file')

    def handle(self, *args, **options):
        filename = options['xlsx_file']
        
        self.stdout.write(f"Reading from {filename}")
        
        if not os.path.exists(filename):
             self.stdout.write(self.style.ERROR(f"File not found: {filename}"))
             return

        try:
            count = import_alumni_from_xlsx(filename, stdout=self.stdout)
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} alumni'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Import failed: {e}"))
