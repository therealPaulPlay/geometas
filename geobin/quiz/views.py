from django.shortcuts import render

from quiz.airtable_api import get_random_fact, get_specific_fact


def quiz(request, fact_id=None):
    if fact_id:
        fact = get_specific_fact(fact_id)
    else:
        fact = get_random_fact()
    context = {'fact': fact}
    return render(request, 'quiz/question.html', context)


# Fact with formatted notes: rec3BZ4znZPlTNyS0