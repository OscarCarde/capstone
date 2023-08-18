import os

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

def get_avatar_path(instance, filename):
    return f"media/{instance.user.id}/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to=get_avatar_path, blank=True)

    def __str__(self):
        return self.user.username
    


####### Hierarchical directory structure ########

def get_file_upload_path(instance, filename):
    return f"{instance.parent_folder.path}/{filename}"

class Repository(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=300, blank=True)
    created = models.DateField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="repositories")
    collaborators = models.ManyToManyField(User, blank=True, related_name="collaborating")

    @property
    def number_of_collaborators(self):
        return self.collaborators.count()

class Directory(models.Model):
    name = models.CharField(max_length=50)
    parent_folder = models.ForeignKey("self", null= True, blank=True, on_delete=models.CASCADE, related_name="subdirectories")
    parent_repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name="directories")

    @property
    def path(self):
        if not self.parent_folder:
            return f"{self.parent_repository.owner.id}/{self.parent_repository.name}/{self.name}"
        else:
            return f"{self.parent_folder.path}/{self.name}"

class FileModel(models.Model):
    parent_folder = models.ForeignKey(Directory, null= True, blank=True, on_delete=models.CASCADE, related_name="files")
    parent_repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name="contents")
    file = models.FileField(upload_to=get_file_upload_path)

    @property
    def filename(self):
        return os.path.basename(self.file.name)
    
###############################################

class Comment(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="comments")
    file = models.ForeignKey(FileModel, blank=True, null=True, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()