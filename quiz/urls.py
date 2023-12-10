from django.urls import path

from . import views

urlpatterns = [
    path('<slug:fact_uuid>/q/', views.question, name='question'),
    path('<slug:fact_uuid>/a/', views.answer, name='answer'),
    path('', views.quiz, name='quiz'),
]