from django.contrib import admin
from .models import PostModel,StoryModel,NotificationModel,FavoritePosts
# Register your models here.

admin.site.register(PostModel)
admin.site.register(StoryModel)
admin.site.register(NotificationModel)
admin.site.register(FavoritePosts)