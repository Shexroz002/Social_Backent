from django.db import models
from django.contrib.auth.models import AbstractUser


class ProfileImage(models.Model):
    photo = models.ImageField(null=True,blank=True,upload_to='user_image/',default='user_image/userimage.jpg')
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "sadasd"


class CustomUser(AbstractUser):
    image = models.ManyToManyField(ProfileImage,blank=True,null=True)

    def __str__(self):
        return self.username

class FollowAndFollowingModel(models.Model):
    my_by=models.ForeignKey(CustomUser,related_name='my_by',on_delete=models.CASCADE)
    friend_by=models.ForeignKey(CustomUser,related_name='friend_by',on_delete=models.CASCADE)
    data=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.my_by.username


class MessageFriendModel(models.Model):
    my_user=models.ForeignKey(CustomUser,related_name='my_user',on_delete=models.CASCADE)
    friend_user=models.ForeignKey(CustomUser,related_name='friend_user',on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.my_user.username
