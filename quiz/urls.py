from django.urls import path

from . import views

urlpatterns = [
    path('<slug:quiz_session_uuid>/<slug:fact_uuid>/q/', views.question, name='question'),
    path('<slug:quiz_session_uuid>/<slug:fact_uuid>/a/', views.answer, name='answer'),
    path('<slug:quiz_session_uuid>/<slug:fact_uuid>/r/', views.rate_fact, name='rate'),
    path('<slug:quiz_session_uuid>/summary/', views.summary, name='summary'),
    path('<slug:quiz_session_uuid>/next/', views.continue_quiz, name='continue_quiz'),
    path('<slug:quiz_uuid>/start/', views.start_quiz, name='start_quiz'),
]