from django.urls import path

from . import views

urlpatterns = [
    path('countries/<slug:country_slug>/', views.country, name='country'),
    path('regions/<slug:region_slug>/', views.region, name='region'),
    path('categories/<slug:category_slug>/', views.category, name='category'),
    path('', views.metas_index, name='metas_index'),
]