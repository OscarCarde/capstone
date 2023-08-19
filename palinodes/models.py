import os

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

def get_avatar_path(instance, filename):
    return f"media/{instance.user.id}/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    description = models.TextField(default="", max_length=300, blank=True)
    avatar = models.ImageField(upload_to=get_avatar_path, blank=True)

    def __str__(self):
        return self.user.username
    


####### Hierarchical directory structure ########
class Parent(models.Model):
    name = models.CharField(max_length=50)

    def path(self):
        pass

    def __str__(self):
        return self.name

def get_file_upload_path(instance, filename):
    return f"{instance.parent.path}/{filename}"

class Repository(Parent):
    #name = models.CharField(max_length=50)
    description = models.TextField(max_length=300, blank=True)
    created = models.DateField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="repositories")
    collaborators = models.ManyToManyField(User, blank=True, related_name="collaborating")

    @property
    def number_of_collaborators(self):
        return self.collaborators.count()
    
    @property
    def path(self):
        return f"{self.owner.id}/{self.name}"
    
    def __str__(self):
        return self.name

class Directory(Parent):
    #name = models.CharField(max_length=50)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name="subdirectories")

    @property
    def path(self):
        return f"{self.parent.path}/{self.name}"

class FileModel(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to=get_file_upload_path)

    @property
    def filename(self):
        return os.path.basename(self.file.name)
    
    def __str__(self):
        return self.filename
###############################################

class Comment(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="comments")
    file = models.ForeignKey(FileModel, blank=True, null=True, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()