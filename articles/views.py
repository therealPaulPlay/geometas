from django.shortcuts import render
import copy

from quiz.models import Country, Fact
from articles.data.eastern_europe_fact_ids import EASTERN_EUROPE_FACT_IDS


def country_coverage(request):
    country_count = Country.objects.count()
    context = {
        'countries': Country.objects.all().order_by('region__sort_order', 'name').select_related('quiz', 'region__quiz'),
        'country_count': country_count,
        'html_meta_title': "Geoguessr Country Coverage",
        'html_meta_description': "In Geoguessr you can encounter up to %s countries. Learn the Geoguessr metas for each country to become a Geoguessr champion." % country_count,
        'html_meta_image_url': request.build_absolute_uri('/static/seo/country_coverage.png'),
    }
    return render(request, 'articles/country_coverage.html', context)


def driving_direction(request):
    context = {
        'countries': Country.objects.all().order_by('name').select_related('quiz'),
        'html_meta_title': "Driving direction in Geoguessr",
        'html_meta_description': "The direction of traffic is a key meta in Geoguessr. Learn the driving direction for each country to become a Geoguessr champion.",
        'html_meta_image_url': request.build_absolute_uri('/static/seo/driving_direction.png'),
    }
    return render(request, 'articles/driving_direction.html', context)


def eastern_europe(request):
    fact_ids = EASTERN_EUROPE_FACT_IDS
    facts_dict = copy.deepcopy(fact_ids)
    for country in fact_ids:
        for fact_type in fact_ids[country]:
            airtable_ids = fact_ids[country][fact_type]
            fact_objects = Fact.objects.filter(airtable_id__in=airtable_ids)
            facts_dict[country][fact_type] = fact_objects
    
    context = {
        'facts': facts_dict,
        'html_meta_title': "Eastern Europe in Geoguessr",
        'html_meta_description': "Eastern Europe is a region in Geoguessr. Learn the countries in Eastern Europe to become a Geoguessr champion.",
        'html_meta_image_url': request.build_absolute_uri('/static/seo/eastern_europe.png'),
    }
    return render(request, 'articles/eastern_europe.html', context)