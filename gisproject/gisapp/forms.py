# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.gis.geos import Point

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['home_address', 'phone_number', 'location']
