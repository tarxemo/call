from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add any additional fields here
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
