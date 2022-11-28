from django.db import models
from users.models import CustomUser
# Create your models here.
class BookType(models.Model):
    book_type = models.CharField(null=False,blank=False,max_length=100)
    start = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.book_type

class PostModel(models.Model):
    post_image = models.ImageField(upload_to = 'post_image/',blank=False,null=False)
    post_title = models.CharField(max_length=300,default='')
    post_name = models.CharField(max_length=300,default='')
    post_creator = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name='post_creator')
    create_by = models.DateTimeField(auto_now_add=True)
    update_by = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(CustomUser,related_name='like')
    post_type = models.ForeignKey(BookType,on_delete=models.CASCADE,null=True,related_name='post_type')
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return self.post_title

class StoryModel(models.Model):
    story_image = models.ImageField(upload_to = 'story_image/',blank=False,null=False)
    story_creator = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name='story_creator')
    create_by = models.DateTimeField(auto_now_add=True)
    seen_user = models.ManyToManyField(CustomUser,related_name='seen_user')
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

class LikeOrPostChoices(models.IntegerChoices):
    LIKE = 0, 'LIKE'
    FOLLOWING = 1, 'FOLLOWING'

class NotificationModel(models.Model):
    notification_visible_to_user = models.ForeignKey(CustomUser,\
                                    related_name='notification_visible_to_user',
                                    on_delete=models.CASCADE,
                                    null=False
                                    )
    following_user = models.ForeignKey(CustomUser,\
                                    related_name='following_user',
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank = True
                                    )
    post_like = models.ForeignKey(PostModel,\
                                    related_name='post_like',
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank = True
                                    )
    follow_or_like = models.IntegerField(choices=LikeOrPostChoices.choices, default=LikeOrPostChoices.LIKE)
    date = models.DateTimeField(auto_now_add=True)

    def _str__(self):
        return self.notification_visible_to_user.username


class FavoritePosts(models.Model):
    client = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=False,blank = True)
    favorite_post = models.ForeignKey(PostModel,on_delete=models.CASCADE,null=False,blank = True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client.username

class ReadedPost(models.Model):
    client = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=False,blank = True)
    post  = models.ForeignKey(PostModel,on_delete=models.CASCADE,null=False,blank = True)
    status = models.BooleanField(default=False)
    date_start = models.DateTimeField(auto_now_add=True)
    date_finish = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client.username

