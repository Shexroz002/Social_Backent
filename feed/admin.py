from django.contrib import admin
from .models import PostModel,StoryModel,NotificationModel,FavoritePosts,ReadedPost,CommentModel,BookType
# Register your models here.

admin.site.register(PostModel)
admin.site.register(StoryModel)
admin.site.register(NotificationModel)
admin.site.register(FavoritePosts)
admin.site.register(ReadedPost)
admin.site.register(CommentModel)
admin.site.register(BookType)