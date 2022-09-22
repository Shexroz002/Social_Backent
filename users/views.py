from feed.models import PostModel
from rest_framework import permissions
from rest_framework import views
from .models import CustomUser,ProfileImage,FollowAndFollowingModel,MessageFriendModel
from .serializers import RegisterSerializer,ProfileSerializer,ProfileImageSerializer,FollowAndFollowingModelSerializer
from rest_framework.response import Response
from rest_framework import status
from feed.serializers import PostSerialzier
from django.shortcuts import get_object_or_404
# Create your views here.
class RegisterView(views.APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            photo = ProfileImage.objects.all().first()
            user.image.add(photo)
            user.save()
            return Response({"register":201},status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class ProfileupdataView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request,pk):
        user = get_object_or_404(CustomUser,id = pk)
        posts = PostModel.objects.filter(post_creator = user)
        post_serializer = PostSerialzier(posts,many=True)
        serializer = ProfileSerializer(user)
        return Response({'user':serializer.data,'post':post_serializer.data},status=status.HTTP_200_OK)
    
    def put(self, request,pk):
        user = get_object_or_404(CustomUser,id = pk)
        serializer = ProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            image_file = request.FILES
            if image_file:
                serializer_file = ProfileImageSerializer(data = image_file)
                serializer_file.is_valid(raise_exception=True)
                photo_file = serializer_file.save()
                user.image.add(photo_file)
                user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class FollowersAPIView(views.APIView):
    def get(self,request,id):
        user = get_object_or_404(CustomUser ,id=id)
        followers = FollowAndFollowingModel.objects.filter(friend_by=user)
        return Response(FollowAndFollowingModelSerializer(followers,many=True).data, status=status.HTTP_200_OK)
    
    def post(self,request,id):
        user=get_object_or_404(CustomUser,id = id)
        friend=FollowAndFollowingModel.objects.filter(my_by=request.user, friend_by=user).exists()
        if friend:
            chat=FollowAndFollowingModel.objects.get(my_by=request.user,friend_by=user)
            chat.delete()
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            follow = FollowAndFollowingModel.objects.create(my_by=request.user, friend_by=user)
            follow.save()
            got=MessageFriendModel.objects.filter(my_user=request.user, friend_user=user).exists()
            sad = FollowAndFollowingModel.objects.filter(my_by=request.user, friend_by=user).exists()
            if not got and sad:
                message = MessageFriendModel.objects.create(my_user=request.user, friend_user=user)
                message.save()
            return Response(status=status.HTTP_201_CREATED)


class FollowingAPIView(views.APIView):
    def get(self,request,id):
        user = get_object_or_404(CustomUser,id = id)
        following = FollowAndFollowingModel.objects.filter(my_by=user)
        return Response(FollowAndFollowingModelSerializer(following,many=True).data , status=status.HTTP_200_OK)
    
    def post(self,request,id):
        user=get_object_or_404(CustomUser,id = id)
        friend=FollowAndFollowingModel.objects.filter(my_by=user, friend_by=request.user).exists()
        if friend:
            chat=FollowAndFollowingModel.objects.get(my_by=user, friend_by=request.user)
            chat.delete()
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            follow = FollowAndFollowingModel.objects.create(my_by=user, friend_by=request.user)
            follow.save()
            got=MessageFriendModel.objects.filter(my_by=user, friend_by=request.user).exists()
            sad = FollowAndFollowingModel.objects.filter(my_account=request.user, friend_account=user).exists()
            if not got and sad:
                message = MessageFriendModel.objects.create(my_by=user, friend_by=request.user)
                message.save()
            return Response(status=status.HTTP_201_CREATED)

class ProfileImageDeleteAPIView(views.APIView):

    def delete(self,request,id):
        image = get_object_or_404(ProfileImage,id = id)
        image.delete()
        return Response(status=status.HTTP_404_NOT_FOUND)

