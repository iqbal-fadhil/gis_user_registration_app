from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserForm, UserProfileForm

from django.shortcuts import render
from .models import UserProfile

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

# Register View
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created for {user.username}!')
            return redirect('profile')
        else:
            messages.error(request, 'There was an error in registration.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login View
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid login credentials.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})    

def user_locations_map(request):
    profiles = UserProfile.objects.exclude(location__isnull=True)

    profile_data = [
        {
            "user": profile.user.username,
            "lat": profile.location.y,  # latitude
            "lng": profile.location.x,   # longitude
            "home_address": profile.home_address,
            "phone_number": profile.phone_number
        }
        for profile in profiles
    ]

    return render(request, 'user_locations_map.html', {
        'profiles': profile_data
    })

from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)
    return redirect('login')    


@login_required
def profile_view(request):
    user_profile = request.user.userprofile
    location = user_profile.location

    lat, lng = (None, None)
    if location:
        lat, lng = location.y, location.x  # GeoDjango stores as (x=lng, y=lat)

    return render(request, 'profile.html', {
        'user': request.user,
        'lat': lat,
        'lng': lng
    })


@login_required
def edit_profile(request):
    user_form = UserForm(instance=request.user)
    profile = request.user.userprofile

    profile_form = UserProfileForm(instance=profile)

    # Prepare lat/lng for JS map
    lat = profile.location.y if profile.location else None
    lng = profile.location.x if profile.location else None

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'lat': lat,
        'lng': lng,
    })
