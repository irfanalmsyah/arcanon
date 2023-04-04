from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    max_age = models.PositiveIntegerField(null=True, blank=True)
    min_age = models.PositiveIntegerField(null=True, blank=True)
    preference = models.CharField(max_length=1, null=True, blank=True)
    
class Room(models.Model):
    name = models.CharField(max_length=32, unique=True)
    requester = models.OneToOneField(User, on_delete=models.CASCADE, related_name='requester')
    responder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responder', null=True, blank=True)

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)