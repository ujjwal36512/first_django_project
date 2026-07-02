from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=True, unique=False)
    full_name = models.CharField(max_length=150, blank=True)
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
    REQUIRED_FIELDS = []
            
    def _str_(self):
        return self.full_name or self.email
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio= models.TextField(blank=True)
    recipes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.full_name}'s Profile"