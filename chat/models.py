from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=64, unique=True)
    channel_name = models.CharField(max_length=128)


class Member(models.Model):
    user = models.ForeignKey(User, 
        on_delete=models.PROTECT)

    room = models.ForeignKey(Room, 
        on_delete=models.PROTECT)


    class Meta:
        unique_together = ('user', 'room')