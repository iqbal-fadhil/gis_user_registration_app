from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    home_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    location = gis_models.PointField(geography=True)

    def __str__(self):
        return self.user.username
