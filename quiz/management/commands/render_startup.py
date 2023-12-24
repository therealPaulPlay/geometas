from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import logging
log = logging.getLogger(__name__)

from quiz.models import QuizSession


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        # Load countries
        from quiz.db_seeds.country_seeder import update_countries
        update_countries()
        
        # Load categories
        from quiz.db_seeds.quiz_seeder import update_categories
        update_categories()
        
        # Load facts
        from quiz.airtable_api import import_all_facts_into_db
        import_all_facts_into_db()
        
        # Load quizzes
        from quiz.db_seeds.quiz_seeder import update_quizzes
        update_quizzes()
        
        # Delete QuizSession without user created 1+ day ago
        old_anon_quiz_sessions = QuizSession.objects.filter(user__isnull=True, created_at__lte=timezone.now()-timedelta(days=1))
        log.info("Deleting %s old anonymous QuizSessions" % old_anon_quiz_sessions.count())
        old_anon_quiz_sessions.delete()
        

        print(">>>>>>>> DONE <<<<<<<<")
