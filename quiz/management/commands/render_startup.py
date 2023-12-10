from django.core.management.base import BaseCommand
import logging
log = logging.getLogger(__name__)

from django.core import management

from quiz.airtable_api import import_all_facts_into_db
from quiz.country_seeder import update_countries



class Command(BaseCommand):

    def handle(self, *args, **options):
        import_all_facts_into_db()
        update_countries()
        print(">>>>>>>> DONE <<<<<<<<")