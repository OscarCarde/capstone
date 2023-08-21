from rest_framework import serializers
from .models import Directory

class RepositorySerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    collaborators_names = serializers.SerializerMethodField()

    def get_collaborators_names(self, obj):
        return list(obj.collaborators.values_list("username", flat=True))

    class Meta:
        model = Directory
        fields = ['name', 'description', 'created', 'owner', 'collaborators_names']
        