from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
USER_TYPE = (
    ("Patient","Patient"),
    ("Doctor","Doctor"),
)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(null=True, blank=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPE, null=True, default=None)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    @property
    def full_name(self):
        """Return the full name (last name + first name)"""
        return f"{self.last_name} {self.first_name}" if self.last_name and self.first_name else self.username

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        email_username, _gmail = self.email.split("@") # name @ gmail.com
        if self.username == "" or self.username == None:
            self.username = email_username

        super(User, self).save(*args, **kwargs)

