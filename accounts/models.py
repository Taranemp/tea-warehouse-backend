from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=15, null=True, blank=True)
    avatar = models.ImageField(upload_to='profile', null=True, blank=True)

    def __str__(self):
        return self.username