from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    class Meta:
        db_table = "user"
    username = models.CharField(max_length=20, unique = True)
    email = models.EmailField(unique=True, null=False, blank=False)
    birth = models.DateField(null=False)
    