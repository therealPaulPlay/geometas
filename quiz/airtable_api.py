from django.conf import settings
from pyairtable import Api
import random


def get_random_fact():
    """ Retrieves a random question from airtable """
    # Get random fact integer
    fact_count = settings.AIRTABLE_FACT_COUNT
    fact_to_get = random.randint(1, fact_count)
    # Send to API
    api = Api(settings.AIRTABLE_API_TOKEN)
    table = api.table(settings.AIRTABLE_APP_ID, settings.AIRTABLE_TABLE_ID)
    response = table.all()
    fact_response = response[fact_to_get-1]
    return deserialize_fact(fact_response)


def get_specific_fact(airtable_id):
    """ Retrieves a random question from airtable """
    api = Api(settings.AIRTABLE_API_TOKEN)
    table = api.table(settings.AIRTABLE_APP_ID, settings.AIRTABLE_TABLE_ID)
    fact_response = table.get(airtable_id)
    print(fact_response)
    return deserialize_fact(fact_response)


def deserialize_fact(fact_response):
    """ Deserializes a fact from API to a dictionary """
    return {
        'question': fact_response['fields']['Fact'],
        'image_url': fact_response['fields']['Image'][0]['url'],
        'countries': fact_response['fields']['Country Name'],
        'type': fact_response['fields']['Category'],
        'notes': fact_response['fields'].get('Notes'),
        'airtable_id': fact_response['id']
    }