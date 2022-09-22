from django.contrib import admin
from .models import PostModel,StoryModel
# Register your models here.

admin.site.register(PostModel)
admin.site.register(StoryModel)
