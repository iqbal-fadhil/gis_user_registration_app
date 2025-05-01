# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserForm, UserProfileForm

from django.shortcuts import render
from .models import UserProfile

def user_locations_map(request):
    profiles = UserProfile.objects.exclude(location__isnull=True)

    profile_data = [
        {
            "user": profile.user.username,
            "lat": profile.location.y,  # latitude
            "lng": profile.location.x   # longitude
        }
        for profile in profiles
    ]

    return render(request, 'user_locations_map.html', {
        'profiles': profile_data
    })


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

from django.contrib.gis.geos import GEOSGeometry

@login_required
def edit_profile(request):
    user_form = UserForm(instance=request.user)
    profile = request.user.userprofile

    # Convert GEOS geometry to WKT string
    if profile.location:
        profile.location = profile.location.wkt

    profile_form = UserProfileForm(instance=profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
