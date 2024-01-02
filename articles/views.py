from django.shortcuts import render
import copy

from quiz.models import Country, Fact


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
    languages = {
        "latin": Fact.objects.get(airtable_id="recqNCngQR2DXrjfz"),
        "both": Fact.objects.get(airtable_id="recS1GDw2ihg83uQv"),
        "cyrillic": Fact.objects.get(airtable_id="recNUAgPDyiNRZEgQ"),
    }
    bollard = {
        "hungary": Fact.objects.filter(category__slug="bollards", country__slug="hungary").first(),
        "slovenia": Fact.objects.filter(category__slug="bollards", country__slug="slovenia").first(),
        "slovakia": Fact.objects.filter(category__slug="bollards", country__slug="slovakia").first(),
    }
    warning_sign = Fact.objects.get(airtable_id="recAhLi7tmiRgab9K")
    directional_signs = {
        "green": Fact.objects.get(airtable_id="recrti8CSFCOOQhHX"),
        "yellow": Fact.objects.get(airtable_id="rec3PWgpmNOrrVPPC"),
        "blue": Fact.objects.get(airtable_id="recDjo4Syy89o6KaO"),
    }
    uniques = {
        "rift": Fact.objects.get(airtable_id="recXrWdj97x8taiOJ"),
        "holey_pole": Fact.objects.get(airtable_id="recL1IehAsZgyVXTV"),
        "albania_license_plate": Fact.objects.get(airtable_id="receyxRDqnI6yxVtu"),
        "ukraine_google_car": Fact.objects.get(airtable_id="rectcLmHQY0fnPnHW"),
        "no_antenna": Fact.objects.get(airtable_id="recKDzh6pC6co9gkm"),
        "hungary_road_marker": Fact.objects.get(airtable_id="recAmDvHOIO0TRSyt"),
        "romania_road_marker": Fact.objects.get(airtable_id="recAcphJ7gaoJUrVd"),
        "slovenia_road_marker": Fact.objects.get(airtable_id="recSAQvo4pRfOP7EX"),
        "romania_yellow_sign": Fact.objects.get(airtable_id="recNRvyTTPazZ12yn"),
        "white_trees": Fact.objects.get(airtable_id="recXkaRoxe8URAuZF"),
        "bulgaria_poles": Fact.objects.get(airtable_id="recI20n5tP82U3zt8"),
        "hungary_hydrant": Fact.objects.get(airtable_id="recLF9YHiUxOB0gml"),
        "croatia_hydrant": Fact.objects.get(airtable_id="recvrPtJKoclKERj6"),
    }
    
    context = {
        'languages': languages,
        'bollards': bollard,
        'warning_signs': warning_sign,
        'directional_signs': directional_signs,
        'uniques': uniques,
        'html_meta_title': "Eastern Europe in Geoguessr",
        'html_meta_description': "Eastern Europe is a region in Geoguessr. Learn the countries in Eastern Europe to become a Geoguessr champion.",
        'html_meta_image_url': request.build_absolute_uri('/static/seo/eastern_europe.png'),
    }
    return render(request, 'articles/eastern_europe.html', context)


def world_map_common_locations(request):
    facts = {
        "hong_kong": Fact.objects.get(airtable_id="recLhAiKhFfBcV4Sd"),
        "midway_atoll": Fact.objects.get(airtable_id="recUgzOC1LIFgzlrS"),
        "xmas_island": Fact.objects.get(airtable_id="recmvCVQEvgwq30sv"),
        "bermuda": Fact.objects.get(airtable_id="receGLe5opxKOJCRy"),
        "madagascar": Fact.objects.get(airtable_id="recYZ7O6Qk1fQMktB"),
        "monaco": Fact.objects.get(airtable_id="recvxUK4ni7oIoMnI"),
        "vienna": Fact.objects.get(airtable_id="rec8iDOvUqIaHLkMo"),
        "singapore": Fact.objects.get(airtable_id="rec9hEYcOwW90WHcq")
    }
    context = {
        'facts': facts,
        'html_meta_title': "The Most Geoguessr World Map Locations",
        'html_meta_description': "Find the most common locations on the Geoguessr world map to become a Geoguessr champion.",
        #'html_meta_image_url': request.build_absolute_uri('/static/seo/world_map_common_locations.png'),
    }
    return render(request, 'articles/world_map_common_locations.html', context)