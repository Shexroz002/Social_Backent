from rest_framework import permissions
from rest_framework import status
from rest_framework import response
from rest_framework import views
from django.shortcuts import get_object_or_404
from .models import PostModel, StoryModel,CommentModel
from .serializers import PostSerialzier,StorySerializer,CommentSerializer
# Create your views here.

class PostCreateAPIViews(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        feed = PostModel.objects.filter(post_creator = request.user)
        return response.Response(PostSerialzier(feed,many=True).data,status = status.HTTP_200_OK)

    def post(self,request):
        print(request.user,request.data)
        serializer = PostSerialzier(data = request.data)
        if serializer.is_valid():
            post_deetail = serializer.save()
            post_deetail.post_creator = request.user
            post_deetail.save()
            return response.Response(PostSerialzier(post_deetail).data,status=status.HTTP_201_CREATED)
        else:
            return response.Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
class PostDetailApiViews(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        feed = get_object_or_404(PostModel,id=id)
        return response.Response(PostSerialzier(feed).data,status = status.HTTP_200_OK)

    def put(self,request,id):
        feed = get_object_or_404(PostModel,id=id)
        serializer_feed = PostSerialzier(feed,data = request.data)
        if serializer_feed.is_valid():
            if feed.post_creator == request.user:
                serializer_feed.save()
                return response.Response(serializer_feed.data,status=status.HTTP_201_CREATED)
            else:
                return response.Response({'error':'You can not update this post. Becouse, You did not create this post.'},status=status.HTTP_400_BAD_REQUEST)
        else:
            return response.Response({'error':serializer_feed.errors},status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        feed = get_object_or_404(PostModel,id=id)
        if feed.post_creator == request.user:
            feed.delete()
            return response.Response({'state':False},status=status.HTTP_404_NOT_FOUND)
        else:
                return response.Response({'error':'You can not delete this post. Becouse, You did not create this post.'},status=status.HTTP_400_BAD_REQUEST)


class PostLikeApiViews(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        feed = get_object_or_404(PostModel,id=id)
        post = feed.like.all()
        user = request.user
        if user in post:
            print(post,'sdw')
            feed.like.remove(user)
            feed.save()
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        else:
            print(post)
            feed.like.add(user)
            feed.save()
            return response.Response(status=status.HTTP_201_CREATED)


class StoryApiViews(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        storys = StoryModel.objects.all()[:6]
        serializer = StorySerializer(storys,many=True)
        return response.Response(serializer.data,status = status.HTTP_200_OK)

    def post(self,request):
        serializer = StorySerializer(data = request.data)
        if serializer.is_valid():
            story_deetail = serializer.save()
            story_deetail.story_creator = request.user
            story_deetail.save()
            return response.Response(StorySerializer(story_deetail).data,status=status.HTTP_201_CREATED)
        else:
            return response.Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class CommentsAPIviews(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        post = get_object_or_404(PostModel,id=id)
        comments = CommentModel.objects.filter(feed_by = post).order_by('-date_by')
        return response.Response(CommentSerializer(comments,many=True).data,status = status.HTTP_200_OK)

    def post(self,request,id):
        post = get_object_or_404(PostModel,id=id)
        user = request.user
        seriazliers = CommentSerializer(data = request.data)
        if seriazliers.is_valid():
            print('otdi')
            new_comment = seriazliers.save()
            new_comment.create_by=user
            new_comment.feed_by=post
            new_comment.save()
            return response.Response(CommentSerializer(new_comment).data,status=status.HTTP_201_CREATED)
        else:
            return response.Response({'eror':seriazliers.errors},status=status.HTTP_400_BAD_REQUEST)



        
        



        
