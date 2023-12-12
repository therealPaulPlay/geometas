from django.shortcuts import render, redirect
import random

from .models import Fact, Quiz


def quiz(request, quiz_uuid):
    quiz = Quiz.objects.get(uuid=quiz_uuid)
    facts = Fact.objects.all()
    if quiz.category:
        facts = facts.filter(category=quiz.category)
    if quiz.countries and quiz.countries.count() > 0:
        facts = facts.filter(countries__in=quiz.countries.all())
    random_fact_id = random.choice(facts).uuid
    return redirect('quiz:question', quiz_uuid=quiz_uuid, fact_uuid=random_fact_id)


def question(request, quiz_uuid, fact_uuid):
    fact = Fact.objects.get(uuid=fact_uuid)
    context = {
        'fact': fact,
        'quiz_uuid': quiz_uuid
    }
    return render(request, 'quiz/question.html', context)


def answer(request, quiz_uuid, fact_uuid):
    fact = Fact.objects.get(uuid=fact_uuid)
    context = {
        'fact': fact,
        'quiz_uuid': quiz_uuid
    }
    return render(request, 'quiz/answer.html', context)


def home(request):
    quizzes_by_meta = Quiz.objects.filter(category__isnull=False)
    quizzes_by_country = Quiz.objects.filter(category__isnull=True)
    context = {
        'quizzes_by_meta': quizzes_by_meta,
        'quizzes_by_country': quizzes_by_country
    }
    return render(request, 'quiz/home.html', context)