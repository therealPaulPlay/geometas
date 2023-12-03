from django.conf import settings
from pyairtable import Api
import random


"""
https://pyairtable.readthedocs.io/en/stable/getting-started.html
"""


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
]