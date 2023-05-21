from django.db import models
from main.models import User
from chat.models import Room
from forum.models import Post, Comment


class Report(models.Model):
    reportee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reportee'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
