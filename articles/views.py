from django.shortcuts import render

from quiz.models import Country

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