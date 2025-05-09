from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    name = models.CharField(max_length=200, null=True)

    email = models.EmailField(unique=True, null=True)

    biography = models.TextField(null=True)

    user_image = models.ImageField(null=True, default="users/avatar.jpg", upload_to="users")

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
