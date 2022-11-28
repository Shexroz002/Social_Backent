from users.models import FollowAndFollowingModel
from .models import PostModel,StoryModel,CommentModel,NotificationModel,FavoritePosts,ReadedPost,BookType
from rest_framework import serializers
from users.serializers import ProfileSerializer



class BookTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookType
        fields="__all__"

class PostSerialzier(serializers.ModelSerializer):
    like = ProfileSerializer(many=True,read_only=True)
    post_creator = ProfileSerializer(read_only=True)
    post_type = BookTypeSerializer(read_only=True)
    class Meta:
        model = PostModel
        fields=['id','post_title','post_type','post_name','post_image','post_creator','create_by','update_by','like','comment_count']
        extra_kwargs = {
            'post_title': {'required': False},
            'post_image': {'required': True},
            
        }
    
    def create(self, validated_data):
        feed = PostModel.objects.create(
            post_title = validated_data.get('post_title'),
            post_image = validated_data['post_image'],
            post_name = validated_data['post_name'],
        )
        feed.save()
        return feed
    
    def update(self,instance,validated_data):
        instance.post_title = validated_data.get('post_title',instance.post_title)
        instance.save()
        return instance

class StorySerializer(serializers.ModelSerializer):
    story_creator = ProfileSerializer(read_only=True)
    seen_user = ProfileSerializer(read_only=True,many=True)
    class Meta:
        model = StoryModel
        fields=['id','story_image','story_creator','create_by','seen_user']
        extra_kwargs = {
            'story_creator': {'required': False},
            'story_image': {'required': False},
            
        }

    def create(self, validated_data):
        story = StoryModel.objects.create(
            story_image = validated_data['story_image'],
        )
        story.save()
        return story

    def update(self,instance,validated_data):
        instance.story_image = validated_data.get('story_image',instance.story_image)
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    create_by = ProfileSerializer(read_only=True)
    class Meta:
        model = CommentModel
        fields='__all__'
        extra_kwargs = {
            'feed_by': {'required': False},
            'create_by': {'required': False},
            
        }
    def create(self, validated_data):
        comments = CommentModel.objects.create(
            comment = validated_data['comment'],
        )
        comments.save()
        return comments


class NotificationsSerializers(serializers.ModelSerializer):
    # notification_visible_to_user = ProfileSerializer()
    following_user = ProfileSerializer()
    post_like = PostSerialzier()

    class Meta:
        model = NotificationModel
        fields = "__all__"

class FavoritePostSerializer(serializers.ModelSerializer):
    favorite_post = PostSerialzier()
    class Meta:
        model = FavoritePosts
        fields=['id','favorite_post']

class ReadedPostSerializer(serializers.ModelSerializer):
    post = PostSerialzier()
    class Meta:
        model = ReadedPost
        fields=['id','post','status']

