from django.conf import settings
from django.utils import timezone
from PIL import Image
from pyairtable import Api
import requests
import boto3
import datetime
import os
import io
import logging
log = logging.getLogger(__name__)

from quiz.models import Country, Fact, Category


"""
https://pyairtable.readthedocs.io/en/stable/getting-started.html
"""


def import_all_facts_into_db():
    """ Imports all facts from airtable into the database """
    api = Api(settings.AIRTABLE_API_TOKEN)
    table = api.table(settings.AIRTABLE_APP_ID, settings.AIRTABLE_TABLE_ID)
    facts = table.all()
    for fact in facts:
        deserialized_fact = deserialize_fact(fact)
        try:
            db_fact = Fact.objects.get(airtable_id=deserialized_fact['airtable_id'])
            # Don't update if fact was updated recently and image url exists (might have been broken)
            if db_fact.updated_at > deserialized_fact['updated_at'] and db_fact.image_url:
                continue
        except Fact.DoesNotExist:
            db_fact = Fact()
        db_fact.answer = deserialized_fact['answer']
        db_fact.country = Country.objects.get(name=deserialized_fact['country'])
        try:
            db_fact.category = Category.objects.get(name=deserialized_fact['category'])
        except Category.DoesNotExist as ex:
            try:
                db_fact.category = Category.objects.get(slug=deserialized_fact['category'].lower())
            except Category.DoesNotExist as ex:
                log.info(f"Category '{deserialized_fact['category']}' does not exist")
                raise ex
        db_fact.notes = deserialized_fact['notes']
        db_fact.airtable_id = deserialized_fact['airtable_id']
        db_fact.google_streetview_url = deserialized_fact['google_streetview_url']
        db_fact.save()
        # Move image from airtable to S3 (needs instance uuid hence post initial save)
        image_name = f"{db_fact.uuid}.jpg"
        move_image_from_airtable_to_spaces(deserialized_fact['image_url'], image_name)
        db_fact.image_url = settings.SPACES_BASE_URL + image_name
        db_fact.save()
        # Check if image is horizontal
        db_fact.image_is_landscape = check_if_image_is_horizontal(db_fact.image_url)
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


def deserialize_fact(fact_response):
    """ Deserializes a fact from API to a dictionary """
    return {
        'updated_at': timezone.make_aware(datetime.datetime.strptime(fact_response['fields']['Last updated'], '%Y-%m-%dT%H:%M:%S.%fZ')),
        'answer': fact_response['fields']['Answer'],
        'image_url': fact_response['fields']['Image'][0]['url'],
        'country': fact_response['fields']['Country Name'][0],
        'category': fact_response['fields']['Category'],
        'notes': fact_response['fields'].get('Notes'),
        'airtable_id': fact_response['id'],
        'google_streetview_url': fact_response['fields'].get('GSV URL'),
    }

def move_image_from_airtable_to_spaces(image_url, image_name):
    """ Moves an image from airtable to Digital Ocean Spaces """
    image_content = download_image_from_airtable(image_url)
    image_content, file_type = resize_image_in_memory(image_content, 1000)
    return upload_image_to_spaces_via_boto(image_content, image_name, file_type)


def download_image_from_airtable(image_url):
    """ Downloads an image from airtable """
    response = requests.get(image_url)
    return response.content


def upload_image_to_spaces_via_boto(image_content, image_name, file_type):
    """ Uploads an image to Digital Ocean Spaces via boto3 """
    bucket_name = settings.SPACES_BUCKET_NAME
    # Add geometas folder prefix to organize files
    spaces_key = f"{settings.SPACES_FOLDER}/{image_name}"
    log.info("Uploading %s to DO Spaces bucket %s" % (spaces_key, bucket_name))
    
    s3_client = boto3.client(
        's3',
        endpoint_url=settings.SPACES_ENDPOINT_URL,
        aws_access_key_id=settings.SPACES_ACCESS_KEY_ID,
        aws_secret_access_key=settings.SPACES_SECRET_ACCESS_KEY,
        region_name=settings.SPACES_REGION
    )
    
    put_kwargs = {
        'Bucket': bucket_name,
        'Key': spaces_key,  # This will be 'geometas/uuid.jpg'
        'Body': image_content,
        'CacheControl': 'public, max-age=2592000',  # 30 days
        'ACL': 'public-read'
    }
    
    if file_type:
        put_kwargs['ContentType'] = f'image/{file_type}'
        
    try:
        s3_client.put_object(**put_kwargs)
        return True
    except Exception as e:
        log.exception("DO Spaces upload failed %s" % e)
        return False

def resize_image_in_memory(image_data, max_size):
    img_format = None
    # Load the image from bytes
    with Image.open(io.BytesIO(image_data)) as img:
        # Get the size of the image
        width, height = img.size

        # Check if the image needs to be resized
        if width > max_size or height > max_size:
            log.info("Resizing image")
            # Calculate the new size maintaining aspect ratio
            if width > height:
                new_width = max_size
                new_height = int(max_size * height / width)
            else:
                new_height = max_size
                new_width = int(max_size * width / height)

            # Resize the image
            img = img.resize((new_width, new_height))

            # Save the resized image to a bytes object for further use
            output = io.BytesIO()
            
            # Preserve PNG alpha channel if it exists
            if img.mode == 'RGBA':
                img_format = 'PNG'  # Use PNG format for images with alpha channel
            else:
                img_format = img.format if img.format else 'JPEG' 
            img.save(output, format=img_format)
            log.info("Resized image to %sx%s" % (new_width, new_height))
            return output.getvalue(), img_format
    
    # Return original image if it wasnt resized
    return image_data, img_format


def check_if_image_is_horizontal(image_url):
    """
    Could combine this with the initial image down/upload to save performance
    But keeping separate for now for clarity
    """
    image_content = requests.get(image_url).content
    with Image.open(io.BytesIO(image_content)) as img:
        width, height = img.size
        if width > height:
            return True
        elif width <= height:
            return False