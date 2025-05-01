from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.gis.geos import Point


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UserProfileForm(forms.ModelForm):
    location = forms.CharField(widget=forms.HiddenInput(), required=False)  # raw POINT string

    class Meta:
        model = UserProfile
        fields = ['home_address', 'phone_number', 'location']

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if location:
            try:
                lng, lat = location.replace("POINT(", "").replace(")", "").split()
                return Point(float(lng), float(lat))
            except Exception as e:
                raise forms.ValidationError("Invalid location format.")
        return None
