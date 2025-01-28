from django.db import models

# Create your models here.
class Member(models.Model):
    name = models.CharField(max_length = 10)
    email = models.TextField(unique = True)
    password = models.TextField(null=True)
    birth = models.DateField(null = True)