from django.contrib.auth.models import AbstractUser
from django.db import models
from users.manager import CustomUserManager


# Define the User model responsible for user accounts
class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)

    # enforces case insensitive login for username
    objects = CustomUserManager()

    # create the string representation of the User object
    def __str__(self):
        return f"{self.username}"

    # ensure the username is saved as all lowercase
    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        self.email = self.email.lower()
        # save the changes to the database
        super().save(*args, **kwargs)
