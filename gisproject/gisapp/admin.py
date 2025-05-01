# admin.py
from django.contrib import admin
from django.contrib.gis import admin as gis_admin
from django.contrib.gis.db import models as gis_models
from leaflet.admin import LeafletGeoAdmin  # Import from leaflet

from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(LeafletGeoAdmin):  # Use LeafletGeoAdmin instead of OSMGeoAdmin
    list_display = ['user', 'home_address', 'phone_number']
