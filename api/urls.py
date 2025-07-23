from django.urls import path
from . import views

urlpatterns = [
    path('countries/<slug:country_slug>/', views.country_metas, name='country_metas'),
    path('categories/<slug:category_slug>/', views.category_metas, name='category_metas'),
]