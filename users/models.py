from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    class Meta:
        db_table = "user"
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=20, unique = True)
    password = models.TextField(max_length= 20, null=False, blank=False)
    birth = models.DateField(null=True, default="2000-01-01")
    