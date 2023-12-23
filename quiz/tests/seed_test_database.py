from django.contrib.auth.models import User
from quiz.models import Fact, Quiz
from quiz.db_seeds.country_seeder import update_countries
from quiz.db_seeds.quiz_seeder import update_categories, update_quizzes


def seed_test_database(num_facts=10):
    update_countries()
    update_categories()
    User.objects.create_user('geotester', 'geotester@geometas.com', 'geotester')
    Quiz.objects.create(name="Geoquiz Test", category_id=1)
    

def create_facts(num_facts=10):
    for i in range(num_facts):
        fact = Fact(
            answer=f"Test Fact {i}",
            category_id=1,
            image_url="https://www.google.com",
            airtable_id=f"rec{i}",
        )
        fact.save()


def create_sample_fact(answer="Test Fact", image_url="https://www.google.com", country_id=1, airtable_id="rec1234567890"):
    fact = Fact(
        answer=answer,
        image_url=image_url,
        country_id=country_id,
        airtable_id=airtable_id,
    )
    fact.save()
    return fact