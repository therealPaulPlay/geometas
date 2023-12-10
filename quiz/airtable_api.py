from django.conf import settings
from pyairtable import Api
import random
import logging
log = logging.getLogger(__name__)

from quiz.models import Country, Fact


"""
https://pyairtable.readthedocs.io/en/stable/getting-started.html
"""

"""
from quiz.airtable_api import import_all_facts_into_db
import_all_facts_into_db()
"""


def import_all_facts_into_db():
    """ Imports all facts from airtable into the database """
    api = Api(settings.AIRTABLE_API_TOKEN)
    table = api.table(settings.AIRTABLE_APP_ID, settings.AIRTABLE_TABLE_ID)
    facts = table.all()
    deserialized_facts = []
    for fact in facts:
        deserialize_fact(fact)
        deserialized_facts.append(deserialize_fact(fact))
    # Create Fact object for each deserialized fact
    for deserialized_fact in deserialized_facts:
        db_fact = Fact.objects.filter(airtable_id=deserialized_fact['airtable_id']).first()
        if not db_fact:
            db_fact = Fact()
        db_fact.answer = deserialized_fact['answer']
        db_fact.image_url = deserialized_fact['image_url']
        db_fact.category = deserialized_fact['category'].lower().replace(" ", "_")
        db_fact.question_type = deserialized_fact['question_type']
        db_fact.difficulty = deserialized_fact['difficulty']
        db_fact.notes = deserialized_fact['notes']
        db_fact.airtable_id = deserialized_fact['airtable_id']
        db_fact.save()
        # Get all countries and add to db_fact.countries
        for country_name in deserialized_fact['countries']:
            country = Country.objects.filter(name=country_name).first()
            if country:
                db_fact.countries.add(country)
            else:
                log.error(f"Country {country_name} not found")
            db_fact.save()

        log.info(f"Fact '{db_fact.airtable_id}' saved")

            
        


def get_random_fact_id():
    """ Retrieves a random question from airtable """
    return random.choice(FACT_IDS)


def get_specific_fact(airtable_id):
    """ Retrieves a random question from airtable """
    api = Api(settings.AIRTABLE_API_TOKEN)
    table = api.table(settings.AIRTABLE_APP_ID, settings.AIRTABLE_TABLE_ID)
    fact_response = table.get(airtable_id)
    #print(fact_response)
    return deserialize_fact(fact_response)


def deserialize_fact(fact_response):
    """ Deserializes a fact from API to a dictionary """
    question_type = fact_response['fields']['QuestionType']
    return {
        'answer': fact_response['fields']['Answer'],
        'image_url': fact_response['fields']['Image'][0]['url'],
        'countries': fact_response['fields']['Country Name'],
        'continents': fact_response['fields'].get('Continents'),
        'category': fact_response['fields']['Category'],
        'difficulty': fact_response['fields']['Difficulty'],
        'question_type': question_type,
        'notes': fact_response['fields'].get('Notes'),
        'airtable_id': fact_response['id'],
        'question': get_question_from_category(question_type)
    }


def get_question_from_category(question_type):
    return {
        "SingleCountry": "Which country is this?",
        "MultipleCountry": "Which countries are these?",
        "SingleContinent": "Which continent is this?",
        "MultipleContinent": "Which continents are these?",
        "NoAnswer": "General learning: did you know this?"
    }[question_type]


FACT_IDS = [
    'rec3BZ4znZPlTNyS0',
    'rec83RapqnhMi3SPp',
    'rec9hEYcOwW90WHcq',
    'recAZHRPIqsU0TBPq',
    'recAeDyESkuueV7Tr',
    'recBj8aFVfcMt8KVz',
    'recCS5u7xRUuELSB2',
    'recFlca195ghowMIu',
    'recIlL6wXQftTnnQP',
    'recJ7STLWjM2rEIGx',
    'recKWflmMHzNH6CJI',
    'recL9lsqoDQb2xkLN',
    'recRCGznGerk5GK2S',
    'recRwEJ1BGS2mcnhW',
    'recZCTHLn1KU4cddm',
    'recZjUf6lFJKJDHsM',
    'recZvIZwZGSVXjXyo',
    'recbKD4hGMSmQrs8Z',
    'recccRZw8zGdHIEQv',
    'recctMSnmyCCajGgC',
    'recdKb67HYla0jhix',
    'recff0Ik4skDcyhj5',
    'recgjxMfXrSmTuBNj',
    'reclO1QGQHEPCqR5B',
    'recmHCmyQnR5o3x4p',
    'recogJ0qW1Rbnq3I3',
    'recpXfiu3NRS6Z7DN',
    'recpYqx87zFyIp7lm',
    'recqNVTm5ARuNw2Ib',
    'recrd6CTbB7mW23hS',
    'recvK7WY4F6g3yw4U',
    'recyAbFeV3B4Oj7Xu',
    'recVHlQ0IvQiPuAAO',
    'recKOGvz1jM44LPLT',
    'rec8XXrnLRGgiypLQ',
]