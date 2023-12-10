from django.shortcuts import render, redirect
import random

from .models import Fact


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




# Fact with formatted notes: rec3BZ4znZPlTNyS0