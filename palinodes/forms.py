from django.forms import ModelForm
from .models import Directory

class RepositoryForm(ModelForm):
    
    class Meta:
        model = Directory
        fields = ["name", "description", "collaborators"]

    