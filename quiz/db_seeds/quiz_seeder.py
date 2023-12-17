import logging
log = logging.getLogger(__name__)

from quiz.models import Quiz, Country, Region


"""
from quiz.db_seeds.quiz_seeder import create_initial_quizzes
create_initial_quizzes()
"""


def create_initial_quizzes():
    
    # Category Quizzes

    # Creat category quizzes
    CATEGORIES_TO_QUIZ = [
        ("bollards", "Bollards"), 
        ("license_plates", "License Plates"), 
        ("language", "Language"), 
        ("poles", "Poles"), 
        ("google_car", "Google Car"),
    ]
    for category in CATEGORIES_TO_QUIZ:
        # Name
        quiz_name = category[1]

        # Get or create quiz
        quiz_db = Quiz.objects.filter(name=quiz_name).first()
        if quiz_db:
            quiz_db.category = category[0]
        else:
            quiz_db = Quiz.objects.create(name=quiz_name, category=category)    
        log.info(f"Quiz {quiz_name} updated")
    
    # Delete old category quizzes
    db_quizzes = Quiz.objects.filter(category__isnull=False)
    category_names = [category[1] for category in CATEGORIES_TO_QUIZ]
    for db_quiz in db_quizzes:
        if db_quiz.name not in category_names:
            db_quiz.delete()
            log.info(f"Quiz {db_quiz.name} deleted")
    

    # Country Quizzes
    # Create one quiz for each Country region 
    
    # Get distinct regions from Country objects that are not empty strings
    regions = Region.objects.all()
    
    for region in regions:
        # Name
        quiz_name = region.name

        # Get or create quiz
        quiz_db = Quiz.objects.filter(name=quiz_name).first()
        if not quiz_db:
            quiz_db = Quiz.objects.create(name=quiz_name)    
        
        # Set all countries in region
        countries = Country.objects.filter(region=region)
        quiz_db.countries.set(countries)

        log.info(f"Quiz {quiz_name} updated")
    
    # Delete old country quizzes
    db_quizzes = Quiz.objects.filter(category__isnull=True)
    region_names = [region.name for region in regions]
    for db_quiz in db_quizzes:
        if db_quiz.name not in region_names:
            db_quiz.delete()
            log.info(f"Quiz {db_quiz.name} deleted")
    
    # Compute and set the number of facts for each quiz
    for quiz in Quiz.objects.all():
        quiz.update_num_facts()
        