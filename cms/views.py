from django.shortcuts import render

from quiz.models import Country, Fact, Region, Category, Quiz, QuizSession



def metas_index(request):
    # Get in_progress quiz session of this user
    quiz_session = None
    if request.user:
        try:
            quiz_session = QuizSession.objects.get(
                user_id=request.user.id,
                state="in_progress"
            )
        except QuizSession.DoesNotExist:
            pass
    
    # Get total fact count
    total_fact_count = Fact.objects.all().count()

    context = {
        'countries': Country.objects.all().order_by('name'),
        'categories': Category.objects.all().order_by('name'),
        'regions': Region.objects.all().order_by('name'),
        'quiz_session': quiz_session,
        'total_fact_count': total_fact_count
    }
    return render(request, 'cms/metas_index.html', context)


def country(request, country_slug):
    # Get Country
    country = Country.objects.get(slug=country_slug)

    # Get de-duped facts
    facts = country.facts.all().order_by('category')
    facts = list(set(facts))

    # No quizzes yet

    context = {
        'country': country,
        'facts': facts
    }
    return render(request, 'cms/country.html', context)

def region(request, region_slug):
    # Get region countries
    countries = Country.objects.filter(region__slug=region_slug).order_by('name')
    region = countries[0].region

    # Get de-duped facts
    facts = []
    for country in countries:
        facts.extend(country.facts.all().order_by('category'))
    facts = list(set(facts))

    # Get related quiz
    try:
        quiz = Quiz.objects.get(name=region.name)
    except Quiz.DoesNotExist:
        quiz = None

    context = {
        'region': region,
        'facts': facts,
        'quiz': quiz
    }
    return render(request, 'cms/region.html', context)

def category(request, category_slug):
    # Get category
    category = Category.objects.get(slug=category_slug)

    # Get facts (no dupes because its not M2M)
    facts = Fact.objects.filter(category=category)

    # Get related quiz
    try:
        quiz = Quiz.objects.get(category=category)
    except Quiz.DoesNotExist:
        quiz = None

    context = {
        'category': category,
        'facts': facts,
        'quiz': quiz
    }
    return render(request, 'cms/category.html', context)