from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

# Create your models here.

class User(AbstractUser):
    def get_absolute_url(self):
        return reverse("blog:profile", kwargs={"username": self.username})