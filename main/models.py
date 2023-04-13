from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True, choices=[('M', 'Male'), ('F', 'Female')])
    age_pref = models.IntegerField(null=True, blank=True, choices=[
            (0, 'Same'),
            (1, 'Younger'),
            (2, 'Older'),
            (3, 'Younger or Same'),
            (4, 'Older or Same'),
            (5, 'Younger or Older'),
        ])
    gender_pref = models.CharField(max_length=1, null=True, blank=True, choices=[('M', 'Male'), ('F', 'Female')])