from django.urls import path

from . import views

urlpatterns = [
    path('auth0/callback/', views.auto0_callback, name='auth0_callback'),
    path('auth0/logout/', views.auto0_logout, name='auth0_logout'),
]