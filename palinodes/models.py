import os

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

def get_avatar_path(instance, filename):
    return f"{instance.user.id}/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    description = models.TextField(default="", max_length=300, blank=True)
    avatar = models.ImageField(upload_to=get_avatar_path, blank=True)

    @property
    def repositories(self):
        return Directory.objects.filter(owner=self.user, parent = None)

    def __str__(self):
        return self.user.username
    


####### Hierarchical directory structure ########
def get_file_upload_path(instance, filename):
        return f"{instance.parent.path}/{filename}"

class Directory(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=300, blank=True, null=True)
    created = models.DateField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="directories")
    collaborators = models.ManyToManyField(User, blank=True, related_name="collaborating")
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE, related_name="subdirectories")

    @property
    def number_of_collaborators(self):
        return self.collaborators.count()
    
    @property
    def path(self) -> str:
        '''recursively retreives the path of the instance directory'''
        if not self.parent:
            return f"{self.owner.id}/{self.name}"
        else:
            return f"{self.parent.path}/{self.name}"
        
    @property
    def is_repository(self):
        return self.parent == None
    
    def __str__(self):
        return f"REPOSITORY: {self.name}" if self.is_repository else self.name


class FileModel(models.Model):
    parent = models.ForeignKey(Directory, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to=get_file_upload_path)

    @property
    def filename(self):
        return os.path.basename(self.file.name)
    
    @property
    def is_audiofile(self):
        extension3 = self.filename[-3:]
        extension4 = self.filename[-4:]
        return extension3 in ["mp3", "wav", "aac", "m4a", ] or extension4 in ["flac", "aiff"]
    
    def __str__(self):
        return self.filename
    
###############################################

class Comment(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, related_name="comments")
    file = models.ForeignKey(FileModel, blank=True, null=True, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()