from django.conf import settings
from django.utils import timezone
from pyairtable import Api
import requests
import boto3
import datetime
import os
import logging
log = logging.getLogger(__name__)

from quiz.models import Country, Fact, Category


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
        needs_update = check_if_fact_needs_update(fact)
        if not needs_update:
            log.info(f"Fact '{fact['id']}' does not need update")
            continue
        deserialize_fact(fact)
        deserialized_facts.append(deserialize_fact(fact))
    # Create Fact object for each deserialized fact
    for deserialized_fact in deserialized_facts:
        db_fact = Fact.objects.filter(airtable_id=deserialized_fact['airtable_id']).first()
        if not db_fact:
            db_fact = Fact()
        db_fact.answer = deserialized_fact['answer']
        db_fact.category = Category.objects.filter(name=deserialized_fact['category']).first()
        db_fact.question_type = deserialized_fact['question_type']
        db_fact.difficulty = deserialized_fact['difficulty']
        db_fact.notes = deserialized_fact['notes']
        db_fact.airtable_id = deserialized_fact['airtable_id']
        db_fact.save()
        # Move image from airtable to S3 (needs instance uuid hence post initial save)
        image_name = f"{db_fact.uuid}.jpg"
        move_image_from_airtable_to_s3(deserialized_fact['image_url'], image_name)
        db_fact.image_url = settings.AWS_S3_BASE_URL + image_name
        # Get all countries and add to db_fact.countries
        for country_name in deserialized_fact['countries']:
            country = Country.objects.filter(name=country_name).first()
            if country:
                db_fact.countries.add(country)
            else:
                log.error(f"Country {country_name} not found")
            db_fact.save()

        log.info(f"Fact '{db_fact.airtable_id}' saved")
    
    # Check if facts have been deleted
    db_facts = Fact.objects.all()
    db_fact_ids = [db_fact.airtable_id for db_fact in db_facts]
    airtable_fact_ids = [fact['id'] for fact in facts]
    deleted_fact_ids = set(db_fact_ids) - set(airtable_fact_ids)
    for deleted_fact_id in deleted_fact_ids:
        log.info(f"Fact '{deleted_fact_id}' deleted")
        Fact.objects.filter(airtable_id=deleted_fact_id).delete()



def check_if_fact_needs_update(fact_response):
    """ 
    Check last updated time of fact in airtable and database 
    Airtable field: 'Last updated': '2023-12-10T10:35:53.000Z'
    Database: Face.updated_at
    """
    airtable_updated_at = fact_response['fields']['Last updated']
    airtable_updated_at = datetime.datetime.strptime(airtable_updated_at, '%Y-%m-%dT%H:%M:%S.%fZ')
    # Handle timezone 
    airtable_updated_at = timezone.make_aware(airtable_updated_at)
    db_fact = Fact.objects.filter(airtable_id=fact_response['id']).first()
    if db_fact:
        if db_fact.updated_at < airtable_updated_at:
            log.info(f"Fact '{fact_response['id']}' updating: last updated at {airtable_updated_at} and DB fact last updated at {db_fact.updated_at}")
            return True
        else:
            log.info(f"Fact '{fact_response['id']}' NOT updating: last updated at {airtable_updated_at} and DB fact last updated at {db_fact.updated_at}")
            return False
    else:
        log.info(f"Fact '{fact_response['id']}' needs to be created")
        return True
        

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
        'airtable_id': fact_response['id']
    }


def move_image_from_airtable_to_s3(image_url, image_name):
    """ Moves an image from airtable to S3 """
    image_content = download_image_from_airtable(image_url)
    return upload_image_to_s3_via_boto(image_content, image_name)


def download_image_from_airtable(image_url):
    """ Downloads an image from airtable """
    response = requests.get(image_url)
    return response.content


def upload_image_to_s3_via_boto(image_content, image_name):
    """ Uploads an image to S3 via boto """
    bucket_name = settings.AWS_S3_IMAGE_STORAGE_BUCKET_NAME
    log.info("Uploading %s to S3 bucket %s" % (image_name, bucket_name))
    s3 = boto3.resource(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', settings.AWS_ACCESS_KEY_ID),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', settings.AWS_SECRET_ACCESS_KEY)
    )
    s3_object = s3.Object(bucket_name, image_name)
    try:
        s3_object.put(Body=image_content)
        log.info("S3 upload successful")
    except Exception as e:
        log.exception("S3 upload failed %s" % e)
        return False
    return True 