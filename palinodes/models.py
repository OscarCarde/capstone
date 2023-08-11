from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="media/avatar", blank=True)


####### Hierarchical directory structure ########

def get_file_upload_path(instance, filename):
    return f"{instance.parent_folder.path}/{filename}"

class Repository(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="repositories")
    collaborators = models.ManyToManyField(User, blank=True, related_name="collaborating")

class Directory(models.Model):
    name = models.CharField(max_length=50)
    parent_folder = models.ForeignKey("self", null= True, blank=True, on_delete=models.CASCADE, related_name="subdirectories")
    parent_repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name="directories")

    @property
    def path(self):
        if not self.parent_folder:
            return f"{self.parent_repository.name}/{self.name}"
        else:
            return f"{self.parent_folder.path}/{self.name}"

class File(models.Model):
    parent_folder = models.ForeignKey(Directory, null= True, blank=True, on_delete=models.CASCADE, related_name="files")
    parent_repository = models.ForeignKey(Repository, on_delete=models.CASCADE, related_name="contents")
    file = models.FileField(upload_to=get_file_upload_path)

    def path(self):
        return self.file.url
    
###############################################

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="comments")
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()