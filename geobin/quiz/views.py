from django.shortcuts import render
from django.conf import settings

from quiz.airtable_api import get_question

def quiz(request):
    fact = get_question()
    context = {'fact': fact}
    return render(request, 'quiz/question.html', context)