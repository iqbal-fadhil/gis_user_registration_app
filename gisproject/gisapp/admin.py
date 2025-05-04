from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'home_address', 'phone_number')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Superusers can see all
        if request.user.is_superuser:
            return qs
        # Staff users only see their own profile
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        # Only allow users to change their own profile
        return obj.user == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        # Only allow users to delete their own profile
        return obj.user == request.user or request.user.is_superuser

admin.site.register(UserProfile, UserProfileAdmin)
