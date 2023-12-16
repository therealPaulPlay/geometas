from django.shortcuts import render

from quiz.models import Country, Fact

def home(request):
    return render(request, 'cms/home.html')
