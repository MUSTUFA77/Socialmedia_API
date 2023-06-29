from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    bio = models.CharField(max_length=250)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()