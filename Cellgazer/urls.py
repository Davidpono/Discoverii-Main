from django.contrib import admin
from django.urls import path
from .import views
app_name = 'Cellgazer'  # This sets the namespace for the app

urlpatterns = [
    path('Cellgazer/', views.cell_view, name='cell_view'),
    path('Cellgazer/conf', views.conf, name='conf_view'),
    path('Cellgazer/ldemo', views.ldemo, name='ldemo_view'),
    path('Cellgazer/mpaper', views.mpaper, name='mpaper_view'),
    path('Cellgazer/lpre', views.lpre, name='lpre_view'),
    # Other URL patterns for the DND app...
]
