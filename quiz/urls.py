from django.urls import path

from . import views

urlpatterns = [
    path('<slug:fact_id>/', views.quiz, name='quiz_specific_id'),
    path('', views.quiz, name='quiz'),
]