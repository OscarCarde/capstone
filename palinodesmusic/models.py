from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

class Song(models.Model):
    name = models.CharField(max_length=50)
    lyrics = models.TextField()
    tempo = models.PositiveIntegerField()
    file = models.FileField()

    @property
    def length(self):
        return 1.0 
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="comments")
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()