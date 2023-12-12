from django.shortcuts import render, redirect
import random

from .models import Fact, Quiz


def quiz(request, fact_id=None):
    # Get a random Fact uuid from quiz.models.Fact
    facts = Fact.objects.all()
    random_fact_id = random.choice(facts).uuid
    return redirect('quiz:question', fact_uuid=random_fact_id)


def question(request, fact_uuid):
    fact = Fact.objects.get(uuid=fact_uuid)
    context = {'fact': fact}
    return render(request, 'quiz/question.html', context)


def answer(request, fact_uuid):
    fact = Fact.objects.get(uuid=fact_uuid)
    context = {'fact': fact}
    return render(request, 'quiz/answer.html', context)


def home(request):
    quizzes_by_meta = Quiz.objects.filter(category__isnull=False)
    quizzes_by_country = Quiz.objects.filter(category__isnull=True)
    context = {
        'quizzes_by_meta': quizzes_by_meta,
        'quizzes_by_country': quizzes_by_country
    }
    return render(request, 'quiz/home.html', context)