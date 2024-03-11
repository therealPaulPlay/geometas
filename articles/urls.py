from django.urls import path

from . import views

urlpatterns = [
    path('geoguessr_country_coverage', views.country_coverage, name='country_coverage'),
    path('driving_direction', views.driving_direction, name='driving_direction'),
    path('eastern_europe', views.eastern_europe, name='eastern_europe'),
    path('world_map_common_locations', views.world_map_common_locations, name='world_map_common_locations'),
    path('south_african_countries', views.south_african_countries, name='south_african_countries'),
    path('latin_america', views.latin_america, name='latin_america'),
    path('nordics', views.nordics, name='nordics'),
    path('australia_new_zealand', views.australia_new_zealand, name='australia_new_zealand'),
    path('south_east_asia', views.south_east_asia, name='south_east_asia'),
    path('baltics', views.baltics, name='baltics'),
]