from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Directory)
admin.site.register(FileModel)
admin.site.register(Comment)