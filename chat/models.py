from django.db import models
from main.models import User


class Room(models.Model):
    name = models.CharField(max_length=32, unique=True)
    requester = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='requester'
    )
    responder = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='responder',
        null=True,
        blank=True
    )
    reveal = models.BooleanField(default=False)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
