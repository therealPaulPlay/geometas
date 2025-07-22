import logging
log = logging.getLogger(__name__)

from quiz.models import Quiz, Country, Region, Category
from quiz.db_seeds.openai_content import OPENAI_CATEGORIES


CATEGORY_CHOICES = [
    ('coverage', 'Coverage'), 
    ('driving_direction', 'Driving Direction'), 
    ('google_car', 'Google Car'), 
    ('language', 'Language'), 
    ('license_plate', 'License Plate'), 
    ('bollards', 'Bollards'), 
    ('street_markings', 'Street Markings'), 
    ('street_name', 'Street Name'), 
    ('street_sign', 'Street Sign'), 
    ('poles', 'Poles'), 
    ('other', 'Other'), 
    ('cars', 'Cars'), 
    ('buildings', 'Buildings'), 
    ('flora', 'Flora'),
    ('guardrails', 'Guardrails'),
    ('chevrons', 'Chevrons'),
    ('milestones', 'Milestone Markers'),
    ('signposts', 'Sign Posts'),
]


def update_categories():
    # Create Categories
    for input_category in CATEGORY_CHOICES:
        category_slug = input_category[0]
        category_name = input_category[1]
        
        # Check if description exists in OPENAI_CATEGORIES
        if category_slug not in OPENAI_CATEGORIES:
            log.warning(f"No description found for category '{category_slug}' in OPENAI_CATEGORIES")
            description = ""
        else:
            description = OPENAI_CATEGORIES[category_slug]
        
        category_db = Category.objects.filter(slug=category_slug).first()
        if category_db:
            category_db.name = category_name
            category_db.description = description
            category_db.save()
        else:
            Category.objects.create(
                name=category_name,
                slug=category_slug,
                description=description
            )
            log.info(f"Category {category_name} created")
    
    # Delete Categories
    db_categories = Category.objects.all()
    input_category_slugs = [input_category[0] for input_category in CATEGORY_CHOICES]
    for db_category in db_categories:
        if db_category.slug not in input_category_slugs:
            if db_category.quiz:
                db_category.quiz.delete()
            db_category.delete()
            log.info(f"Category {db_category.name} deleted")


def update_quizzes():    
    # Category Quizzes
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
            log.info(f"Quiz {quiz_name} created")
        
        # Add Quiz FK to Category
        category.quiz = quiz_db
        category.save()


    # Region Quizzes
    regions = Region.objects.all()
    for region in regions:
        # Name
        quiz_name = region.name

        # Get or create quiz
        quiz_db = Quiz.objects.filter(name=quiz_name).first()
        if not quiz_db:
            quiz_db = Quiz.objects.create(name=quiz_name)  
            log.info(f"Quiz {quiz_name} created")
        
        # Set all countries in region
        countries = Country.objects.filter(region=region)
        quiz_db.countries.set(countries)
        
        # Add Quiz FK to Region
        region.quiz = quiz_db
        region.save()
    
    
    # Country Quizzes
    countries = Country.objects.all()
    for country in countries:
        # Name
        quiz_name = country.name

        # Get or create quiz
        quiz_db = Quiz.objects.filter(name=quiz_name).first()
        if not quiz_db:
            quiz_db = Quiz.objects.create(name=quiz_name)    
            log.info(f"Quiz {quiz_name} created")
        
        # Set country
        quiz_db.countries.set([country,])
        
        # Add Quiz FK to Country
        country.quiz = quiz_db
        country.save()
    
    
    # Create 'Random' quiz for all facts
    random_quiz_name = Quiz.RANDOM_QUIZ_NAME
    quiz_db, created = Quiz.objects.get_or_create(name=random_quiz_name)
    if created:
        log.info(f"Quiz {random_quiz_name} created")
    else:
        log.info(f"Quiz {random_quiz_name} already exists")
    
    
    # Compute and set the number of facts for each quiz
    for quiz in Quiz.objects.all():
        quiz.update_num_facts()
        
        # Delete quiz if no facts
        quiz = Quiz.objects.get(uuid=quiz.uuid)
        if quiz.num_facts == 0:
            quiz.delete()
            log.info(f"Quiz {quiz.name} deleted")