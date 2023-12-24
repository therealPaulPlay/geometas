from django.shortcuts import render

from quiz.models import Country

def country_coverage(request):
    country_count = Country.objects.count()
    context = {
        'countries_europe': Country.objects.filter(continent="Europe").order_by('region', 'name').select_related('quiz', 'region__quiz'),
        'countries_asia': Country.objects.filter(continent="Asia").order_by('region', 'name').select_related('quiz', 'region__quiz'),
        'countries_americas': Country.objects.filter(continent__icontains="America").order_by('region', 'name').select_related('quiz', 'region__quiz'),
        'countries_row': Country.objects.all().exclude(continent="Europe").exclude(continent="Asia").exclude(continent__icontains="America").order_by('region', 'name').select_related('quiz', 'region__quiz'),
        'country_count': country_count,
        'html_meta_title': "Geoguessr Country Coverage",
        'html_meta_description': "In Geoguessr you can encounter up to %s countries. Learn the Geoguessr metas for each country to become a Geoguessr champion." % country_count,
        'html_meta_image_url': request.build_absolute_uri('/static/seo/country_coverage.png'),
    }
    return render(request, 'articles/country_coverage.html', context)