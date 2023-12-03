from django.shortcuts import render, redirect

from quiz.airtable_api import get_random_fact_id, get_specific_fact


def quiz(request, fact_id=None):
    random_fact_id = get_random_fact_id()
    return redirect('quiz:question', fact_id=random_fact_id)


def question(request, fact_id):
    fact = get_specific_fact(fact_id)
    context = {'fact': fact}
    return render(request, 'quiz/question.html', context)

def answer(request, fact_id):
    fact = get_specific_fact(fact_id)
    context = {'fact': fact}
    return render(request, 'quiz/answer.html', context)




# Fact with formatted notes: rec3BZ4znZPlTNyS0