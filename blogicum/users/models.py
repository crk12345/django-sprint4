from django.db import models

# Create your models here.

class User(AbstractUser):
    def get_absolute_url(self):
        return reverse("blog:profile", kwargs={"username": self.username})