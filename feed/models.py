from django.db import models
from users.models import CustomUser
# Create your models here.

class PostModel(models.Model):
    post_image = models.ImageField(upload_to = 'post_image/',blank=False,null=False)
    post_title = models.CharField(max_length=300,default='')
    post_creator = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name='post_creator')
    create_by = models.DateTimeField(auto_now_add=True)
    update_by = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(CustomUser,blank=True,null=True,related_name='like')

    def __str__(self):
        return self.post_title

class StoryModel(models.Model):
    story_image = models.ImageField(upload_to = 'story_image/',blank=False,null=False)
    story_creator = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name='story_creator')
    create_by = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        story = 'story'
        return self.story_image.url

class CommentModel(models.Model):
    feed_by = models.ForeignKey(PostModel,on_delete=models.CASCADE,related_name='feed',null=True,)
    create_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='users',null=True,)
    comment = models.CharField(max_length=300)
    date_by = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
