from django.shortcuts import render

from quiz.models import Country, Fact, CATEGORY_CHOICES


def home(request):
    return render(request, 'cms/home.html')

def metas_index(request):
    context = {
        'countries': Country.objects.filter(slug__isnull=False).exclude(slug='').order_by('name'),
        'categories': CATEGORY_CHOICES,
        'regions': Country.objects.filter(region__isnull=False).exclude(region='').values_list('region', 'region_slug').distinct(),
    }
    return render(request, 'cms/metas_index.html', context)


def country(request, country_slug):
    country = Country.objects.get(slug=country_slug)
    facts = country.facts.all().order_by('category')
    # Dedupe facts
    facts = list(set(facts))
    context = {
        'country': country,
        'facts': facts
    }
    return render(request, 'cms/country.html', context)

def region(request, region_slug):
    countries = Country.objects.filter(region_slug=region_slug).order_by('name')
    facts = []
    for country in countries:
        facts.extend(country.facts.all().order_by('category'))
    # Dedupe facts
    facts = list(set(facts))
    context = {
        'region': countries[0].region,
        'facts': facts
    }
    return render(request, 'cms/region.html', context)

def category(request, category_slug):
    facts = Fact.objects.filter(category=category_slug)
    category_name = dict(CATEGORY_CHOICES)[category_slug]
    context = {
        'category': category_name,
        'facts': facts
    }
    return render(request, 'cms/category.html', context)