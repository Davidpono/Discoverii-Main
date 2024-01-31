from django.contrib import admin
from django.urls import path
from .import views
app_name = 'about_me'  # This sets the namespace for the app

urlpatterns = [
    path('About/', views.about, name='about'),
]