from rest_framework import serializers
from .models import Directory, FileModel

class RepositorySerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    collaborators_names = serializers.SerializerMethodField()

    def get_collaborators_names(self, obj):
        return list(obj.collaborators.values_list("username", flat=True))

    class Meta:
        model = Directory
        fields = ['name', 'description', 'created', 'owner', 'collaborators_names']
        
class DirectorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Directory
        fields=['pk', 'name']

class FileSerializer(serializers.ModelSerializer):
    filename = serializers.SerializerMethodField()
    fileurl = serializers.SerializerMethodField()
    is_audiofile = serializers.SerializerMethodField()

    def get_is_audiofile(self, obj):
        return obj.is_audiofile
    
    def get_filename(self, obj):
        return obj.filename
    
    def get_fileurl(self, obj):
        return obj.file.url
    
    class Meta:
        model=FileModel
        fields = ['filename', 'fileurl', 'is_audiofile']
