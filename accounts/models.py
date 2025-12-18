# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Base custom user model.
    Extend this model later without breaking the database.
    """

    # Example future-proof fields (commented for now)
    # phone = models.CharField(max_length=20, blank=True, null=True)
    # avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    class Meta:
        db_table = "auth_user"
