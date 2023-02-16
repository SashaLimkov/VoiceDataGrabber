import os

from django.core.management import BaseCommand
from openpyxl import load_workbook

from TatSpeaks.settings import BASE_DIR
from backend.services.originals import create_original, get_first_batch_to_fill, create_first_barch


class Command(BaseCommand):
    help = "Fill first batch to DB"

    def handle(self, *args, **options):
        originals = get_first_batch_to_fill()
        for original in originals:
            create_first_barch(original)
