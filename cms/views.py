from django.shortcuts import render, get_object_or_404
from urllib.parse import urlparse, parse_qs, unquote
import requests
import logging
log = logging.getLogger(__name__)

from quiz.models import Country, Fact, Category, Quiz, QuizSession, Region



def metas_index(request):
    # Get in_progress quiz session of this user
    quiz_session = None
    if request.user.is_authenticated:
        try:
            quiz_session = QuizSession.objects.get(
                user_id=request.user.id,
                state="in_progress"
            )
        except QuizSession.DoesNotExist:
            pass
    
    # Get total fact count
    total_fact_count = Fact.objects.all().count()

    random_quiz, _ = Quiz.objects.get_or_create(name=Quiz.RANDOM_QUIZ_NAME)

    context = {
        'countries': Country.objects.all().order_by('region__sort_order', 'name').select_related('quiz', 'region__quiz'),
        'categories': Category.objects.all().order_by('name').select_related('quiz'),
        'quiz_session': quiz_session,
        'total_fact_count': total_fact_count,
        'random_quiz_uuid': random_quiz.uuid,
        'html_meta_title': None,
        'html_meta_description': 'Become a GeoGuessr champion: find new GeoGuessr metas from Google Streetview around the world and test your knowledge with quizzes.',
        'html_meta_image_url': request.build_absolute_uri('/static/logo/logo.png'),
    }
    return render(request, 'cms/metas_index.html', context)


def country(request, country_slug):
    country = get_object_or_404(Country, slug=country_slug)
    facts = Fact.objects.select_related('country', 'category').filter(country=country).order_by('category')

    context = {
        'country': country,
        'facts': facts,
        'quiz': country.quiz,
        'html_meta_title': country.name,
        'html_meta_description': "Learn the GeoGuessr metas for %s to become a GeoGuessr champion" % country.name,
    }
    return render(request, 'cms/country.html', context)


def region(request, region_slug):
    region = get_object_or_404(Region, slug=region_slug)
    facts = Fact.objects.select_related('country', 'category').filter(country__region=region).order_by('category')

    context = {
        'region': region,
        'facts': facts,
        'quiz': region.quiz,
        'html_meta_title': region.name,
        'html_meta_description': region.description,
    }
    return render(request, 'cms/region.html', context)


def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    facts = Fact.objects.select_related('country', 'category').filter(category=category)

    context = {
        'category': category,
        'facts': facts,
        'quiz': category.quiz,
        'html_meta_title': category.name,
        'html_meta_description': category.description,
    }
    return render(request, 'cms/category.html', context)


def fact_detail(request, fact_uuid):
    fact = get_object_or_404(Fact.objects.select_related('country', 'category'), uuid=fact_uuid)
    fact_title = "%s: %s meta" % (fact.country.name, fact.category.name.lower())

    # Ensure we have latlng for Fact
    if not fact.google_streetview_latlng:
        fact.google_streetview_latlng = get_streetview_latlng(fact.google_streetview_url)
        fact.save()
    
    context = {
        'fact': fact,
        'fact_title': fact_title,
        'html_meta_title': fact_title,
        'html_meta_description': fact.answer,
        'html_meta_image_url': fact.image_url,
    }
    return render(request, 'cms/fact_detail.html', context)


def get_streetview_latlng(url):
    if not url:
        return None
    response = requests.get(url, allow_redirects=True)  
    return parse_viewpoint_from_url(response.url)
    
def parse_viewpoint_from_url(url):
    try:
        # Parse the URL
        parsed_url = urlparse(url)

        # Extract query parameters
        query_params = parse_qs(parsed_url.query)

        # Attempt 1
        viewpoint = query_params.get("viewpoint", [None])[0]
        
        # Attempt 2
        if not viewpoint:
            path = parsed_url.path
            at_symbol_index = path.find('@')
            if at_symbol_index != -1:
                coordinates_part = path[at_symbol_index + 1:]  # Get the part after '@'
                comma_index = coordinates_part.find(',')  # Find the first comma
                second_comma_index = coordinates_part.find(',', comma_index + 1)  # Find the second comma
                if second_comma_index != -1:
                    # Extract everything before the second comma
                    viewpoint = coordinates_part[:second_comma_index]
        
        # Attempt 3
        if not viewpoint:
            google_maps_url = query_params.get('continue', [None])[0]
            if google_maps_url:
                # Decode the URL
                decoded_url = unquote(google_maps_url)
                # Now parse the decoded URL
                parsed_maps_url = urlparse(decoded_url)
                # The coordinates are in the 'viewpoint' parameter
                maps_query_params = parse_qs(parsed_maps_url.query)
                viewpoint = maps_query_params.get('viewpoint', [None])[0]
        
        # Attempt 4
        if not viewpoint:
            maps_url = query_params.get('continue', [''])[0]
            # Further parse the maps URL to extract the coordinates
            maps_parsed = urlparse(maps_url)
            coordinates = maps_parsed.path.split('@')[1].split(',')[0:2]
            viewpoint =  ','.join(coordinates)
        
        if not viewpoint:
            log.error("Could not extract viewpoint from URL: %s" % url)
            return None
        
        return viewpoint
    except Exception as ex:
        log.error("Error extracting viewpoint from URL: %s due to %s" % (url, ex))
        return None