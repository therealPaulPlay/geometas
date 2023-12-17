from django.shortcuts import render

from quiz.models import Country, Fact, Region, Category


def home(request):
    return render(request, 'cms/home.html')

def metas_index(request):
    context = {
        'countries': Country.objects.all().order_by('name'),
        'categories': Category.objects.all().order_by('name'),
        'regions': Region.objects.all().order_by('name'),
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
    countries = Country.objects.filter(region__slug=region_slug).order_by('name')
    facts = []
    for country in countries:
        facts.extend(country.facts.all().order_by('category'))
    # Dedupe facts
    facts = list(set(facts))
    context = {
        'region': countries[0].region.name,
        'facts': facts
    }
    return render(request, 'cms/region.html', context)

def category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    facts = Fact.objects.filter(category=category)
    context = {
        'category': category.name,
        'facts': facts
    }
    return render(request, 'cms/category.html', context)