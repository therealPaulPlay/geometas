from django.conf import settings
from pyairtable import Api
import random
import json

def get_question():
    """ Retrieves a random question from airtable """
    # Get random fact integer
    fact_count = settings.AIRTABLE_FACT_COUNT
    fact_to_get = random.randint(1, fact_count)
    api = Api(settings.AIRTABLE_API_TOKEN)
    table = api.table(settings.AIRTABLE_APP_ID, settings.AIRTABLE_TABLE_ID)
    response = table.all()
    fact_response = response[fact_to_get-1]
    fact = {
        'question': fact_response['fields']['Fact'],
        'image_url': fact_response['fields']['Image'][0]['url'],
        'countries': fact_response['fields']['Country Name'],
        'type': fact_response['fields']['Type'],
        'notes': fact_response['fields'].get('Notes'),
    }
    return fact