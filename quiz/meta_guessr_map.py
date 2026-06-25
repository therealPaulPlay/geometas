from django.conf import settings
import json
import logging
log = logging.getLogger(__name__)

from quiz.models import Fact
from quiz.airtable_api import get_spaces_client
from cms.views import resolve_streetview_url


MAP_S3_KEY = "openguessr-official-maps/meta_guessr.json"


def build_and_upload_meta_guessr_map():
    """ Builds an in-game map of all facts with a location and uploads it to Spaces """
    # Resolving each SV URL is a slow redirect, so count how many we have to log progress
    facts_with_url = [fact for fact in Fact.objects.all() if fact.google_streetview_url]
    log.info("Building meta guessr map from %s facts with a location" % len(facts_with_url))

    locations = []
    for index, fact in enumerate(facts_with_url, start=1):
        if index % 50 == 0:
            log.info("Resolved %s/%s locations" % (index, len(facts_with_url)))
        latlng, heading, panorama_id = resolve_streetview_url(fact.google_streetview_url)
        if not latlng:
            # A URL exists but failed to resolve coords
            log.error("Could not extract location for fact '%s'" % fact.airtable_id)
            continue
        lat, lng = (float(coord) for coord in latlng.split(','))
        locations.append([lat, lng, {
            'heading': heading,
            'panoramaId': panorama_id,
            'meta': {
                'text': fact.answer,
                'note': fact.notes,
                'imageUrl': fact.image_url,
            },
        }])

    log.info("Built meta guessr map with %s locations" % len(locations))
    upload_map_to_spaces(locations)


def upload_map_to_spaces(locations):
    """ Uploads the map JSON to Digital Ocean Spaces via boto3 """
    log.info("Uploading %s to DO Spaces bucket %s" % (MAP_S3_KEY, settings.SPACES_BUCKET_NAME))
    get_spaces_client().put_object(
        Bucket=settings.SPACES_BUCKET_NAME,
        Key=MAP_S3_KEY,
        Body=json.dumps({'locations': locations}),
        ContentType='application/json',
        ACL='public-read'
    )
