import logging
log = logging.getLogger(__name__)

from quiz.models import Quiz, Country


"""
from quiz.db_seeds.quiz_seeder import create_initial_quizzes
create_initial_quizzes()
"""


def create_initial_quizzes():
    # Category Quizzes
    CATEGORIES_TO_QUIZ = ["bollards", "license_plates", "language", "poles", "google_car"]
    for category in CATEGORIES_TO_QUIZ:
        # Translate snake case to title case
        quiz_name = category.replace("_", " ").title()

        # Get or create quiz
        quiz_db = Quiz.objects.filter(name=quiz_name).first()
        if quiz_db:
            quiz_db.category = category
        else:
            quiz_db = Quiz.objects.create(name=quiz_name, category=category)    
        log.info(f"Quiz {quiz_name} updated")
    

    # Country Quizzes
    # Create one quiz for each Country region 
    
    # Get distinct regions from Country objects that are not empty strings
    regions = Country.objects.all().values_list('region', flat=True).distinct()
    
    for region in regions:
        # Region name is quiz name, already in title case
        quiz_name = region

        # Get or create quiz
        quiz_db = Quiz.objects.filter(name=quiz_name).first()
        if not quiz_db:
            quiz_db = Quiz.objects.create(name=quiz_name)    
        
        # Set all countries in region
        countries = Country.objects.filter(region=region)
        quiz_db.countries.set(countries)

        log.info(f"Quiz {quiz_name} updated")
    
    # Compute and set the number of facts for each quiz
    for quiz in Quiz.objects.all():
        quiz.update_num_facts()
        