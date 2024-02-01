from django.contrib import admin
from django.urls import path, include
from Iron.viewsfolder import views1, loginview, userprofileviews, workoutviews, actualworkoutview, registerview
from Iron.viewsfolder.api.programapi import WorkoutAPIView
from Iron.viewsfolder.api.user import UserAPIView

app_name = 'Iron'  # This sets the namespace for the app

urlpatterns = [
    path('Iron/', views1.goal, name='goal_view'),
    path('Iron/bbing', views1.bbing, name='bbing_view'),
    path('login/', loginview.login, name='login'),
    path('register/', registerview.register, name='register'),

    path('userProfile/', userprofileviews.userprofile, name='userprofile'),
    path('workout/', workoutviews.workout, name='workout'),
   
    # urls.py
    path('actualworkout/<str:section_param>/', actualworkoutview.actualworkoutview, name='actualworkout'),

    path('api/workouts/', WorkoutAPIView.as_view(), name='workout_api'),
    path('api/login/', UserAPIView.as_view(), name='register_api'),
    path('api/register/', UserAPIView.as_view(), name='login_api'),
    path('api/user/', UserAPIView.as_view(), name='user_api'),
 
    # Other URL patterns for the DND app...
]
