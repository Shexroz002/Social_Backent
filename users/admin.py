from django.contrib import admin
from .models import CustomUser,ProfileImage,FollowAndFollowingModel,MessageFriendModel
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(ProfileImage)

admin.site.register(FollowAndFollowingModel)
admin.site.register(MessageFriendModel)