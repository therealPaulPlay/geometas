import logging
log = logging.getLogger(__name__)

from quiz.models import Quiz, Country


"""
from quiz.db_seeds.quiz_seeder import create_initial_quizzes
create_initial_quizzes()
"""

INPUT_QUIZZES = [
    ("Bollards", "bollards", []),
    ("Nordics", None, ["DK", "FI", "NO", "SE"]),
    ("Baltics", None, ["EE", "LV", "LT"]),
    ("South East Asia", None, ["ID", "LA", "MY", "PH", "SG", "TH"]),
    ("South America", None, ["AR", "BR", "CL", "CO", "PE", "BO", "UY"]),
    ("Central & Eastern Europe", None, ["CZ", "HU", "PL", "SK", "SI", "HR", "RS", "ME", "MK", "BG", "RO", "AL", "UA"]),
]


def create_initial_quizzes():
    for input_quiz in INPUT_QUIZZES:
        print("Looking up quiz %s", input_quiz)
        quiz_db = Quiz.objects.filter(name=input_quiz[0]).first()
        if quiz_db:
            quiz_db.category = input_quiz[1]
        else:
            quiz_db = Quiz.objects.create(
                name=input_quiz[0],
                category=input_quiz[1]
            )
        # Add many-to-many countries from input_quiz[3] list of iso 2 codes, which have to be mapped to Country objects
        quiz_db.countries.set(Country.objects.filter(iso2__in=input_quiz[2]))
        quiz_db.save()
        log.info(f"Quiz {input_quiz[0]} updated")
        