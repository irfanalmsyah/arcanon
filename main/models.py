from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=2, blank=True)
    instagram = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    picture = models.ImageField(upload_to='profile_pics', blank=True)
    gender = models.CharField(
        max_length=1,
        blank=True,
        choices=[('M', 'Male'), ('F', 'Female')]
    )
    age_pref = models.IntegerField(blank=True, null=True, choices=[
            (0, 'Same'),
            (1, 'Younger'),
            (2, 'Older'),
            (3, 'Younger or Same'),
            (4, 'Older or Same'),
            (5, 'Younger or Older'),
        ])
    gender_pref = models.CharField(
        max_length=1,
        blank=True,
        choices=[('M', 'Male'), ('F', 'Female')]
    )

    def isComplete(self):
        return (self.name and
                self.country and
                self.instagram and
                self.twitter and
                self.picture)
