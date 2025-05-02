# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_locations_map, name='user_locations_map'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]