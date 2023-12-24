from django.urls import path

from . import views

urlpatterns = [
    path('geoguessr_country_coverage', views.country_coverage, name='country_coverage'),
]