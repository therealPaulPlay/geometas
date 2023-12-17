import logging
log = logging.getLogger(__name__)

from quiz.models import Quiz, Country, Region, Category


CATEGORY_CHOICES = [
    ("coverage", "Coverage"),
    ("driving_direction", "Driving direction"),
    ("google_car", "Google Car"),
    ("language", "Language"),
    ("license_plate", "License Plate"),
    ("road_lines", "Road Lines"),
    ("settlement_sign", "Settlement Sign"),
    ("bollards", "Bollards"),
    ("street_numbering", "Street Numbering"),
    ("street_markings", "Street Markings"),
    ("street_name", "Street Name"),
    ("street_sign", "Street Sign"),
    ("poles", "Poles"),
    ("other", "Other"),
    ("cars", "Cars"),
    ("pedestrian_crossign_sign", "Pedestrian Crossing Sign"),
    ("buildings", "Buildings"),
    ("flora", "Flora"),
]


def update_categories():
    # Create Categories
    for input_category in CATEGORY_CHOICES:
        category_db = Category.objects.filter(slug=input_category[0]).first()
        if category_db:
            category_db.name = input_category[1]
            category_db.save()
        else:
            Category.objects.create(
                name=input_category[1],
                slug=input_category[0]
            )
        log.info(f"Category {input_category[1]} updated")
    
    # Delete Categories
    db_categories = Category.objects.all()
    input_category_slugs = [input_category[0] for input_category in CATEGORY_CHOICES]
    for db_category in db_categories:
        if db_category.slug not in input_category_slugs:
            db_category.delete()
            log.info(f"Category {db_category.name} deleted")


def update_quizzes():

    # Create Categories
    update_categories()
    
    # Category Quizzes

    # Creat category quizzes
    categories = Category.objects.all()
    for category in categories:
        # Name
        quiz_name = category.name

        # Get or create quiz
        quiz_db = Quiz.objects.filter(name=quiz_name).first()
        if quiz_db:
            quiz_db.category = category
        else:
            quiz_db = Quiz.objects.create(name=quiz_name, category=category)    
        log.info(f"Quiz {quiz_name} updated")
    
    # Delete old category quizzes
    db_quizzes = Quiz.objects.filter(category__isnull=False)
    category_names = [category.name for category in categories]
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
        
        # Delete quiz if no facts
        quiz = Quiz.objects.get(uuid=quiz.uuid)
        if quiz.num_facts == 0:
            quiz.delete()
            log.info(f"Quiz {quiz.name} deleted")
        