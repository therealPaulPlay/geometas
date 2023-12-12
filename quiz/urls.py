from django.urls import path

from . import views

urlpatterns = [
    path('<slug:quiz_uuid>/<slug:fact_uuid>/q/', views.question, name='question'),
    path('<slug:quiz_uuid>/<slug:fact_uuid>/a/', views.answer, name='answer'),
    path('<slug:quiz_uuid>/', views.quiz, name='quiz'),
]