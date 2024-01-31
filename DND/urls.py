from django.contrib import admin
from django.urls import path
from .import views
app_name = 'DND'  # This sets the namespace for the app

urlpatterns = [
     path('base/', views.dnd_view, name='dnd_view'),
     
    # Other URL patterns for the DND app...
    # path('Cellgazer/lpre', views.lpre, name='lpre_view'),
]
