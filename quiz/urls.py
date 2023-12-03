from django.urls import path

from . import views

urlpatterns = [
    path('<slug:fact_id>/q/', views.question, name='question'),
    path('<slug:fact_id>/a/', views.answer, name='answer'),
    path('', views.quiz, name='quiz'),
]