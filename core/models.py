from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=True, unique=False)
    full_name = models.CharField(max_length=150)
    address = models.CharField(blank=True)
    gender = models.CharField(
        max_length=10,
        choices = [
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        blank = True
    )
    contact_number = models.CharField(max_length = 15, blank=True)
    email = models.EmailField(unique=True)
    
    objects = UserManager()

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def save(self, args, **kwargs):              # () means all aruguments
        if not self.username:
            self.username = self.email.split('@')[0]
            super().save(*args, **kwargs)
            
    def _str_(self):
        return self.full_name