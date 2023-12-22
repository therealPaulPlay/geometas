from django.core.management.base import BaseCommand
import logging
log = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        # Load countries
        from quiz.db_seeds.country_seeder import update_countries
        update_countries()

        # Load quizzes
        # Shiuld extract categories here and quiz af end
        from quiz.db_seeds.quiz_seeder import update_quizzes
        update_quizzes()
        
        # Load facts
        from quiz.airtable_api import import_all_facts_into_db
        import_all_facts_into_db()

        # Create a new superuser
        from django.contrib.auth.models import User
        try:
            User.objects.create_superuser('geobin', 'geo@kreuz.de', 'geobin')
        except Exception as e:
            print(e)

        print(">>>>>>>> DONE <<<<<<<<")
