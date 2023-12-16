from django.urls import path

from . import views

urlpatterns = [
    path('<slug:quiz_uuid>/<slug:fact_uuid>/q/', views.question, name='question'),
    path('<slug:quiz_uuid>/<slug:fact_uuid>/a/', views.answer, name='answer'),
    path('<slug:quiz_uuid>/<slug:fact_uuid>/r/', views.rate_fact, name='rate'),
    path('<slug:quiz_uuid>/summary/<slug:quiz_session_uuid>/', views.summary, name='summary'),
    path('<slug:quiz_uuid>/', views.quiz, name='quiz'),
    path('', views.quiz_index, name='quiz_index'),
]