from feed.models import PostModel
from rest_framework import permissions
from rest_framework import views
from .models import CustomUser,ProfileImage,FollowAndFollowingModel,MessageFriendModel
from .serializers import RegisterSerializer,ProfileSerializer,ProfileImageSerializer,FollowAndFollowingModelSerializer
from rest_framework.response import Response
from rest_framework import status
from feed.serializers import PostSerialzier
from django.shortcuts import get_object_or_404
from feed.models import NotificationModel
from django.db.models import Q
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
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        user = get_object_or_404(CustomUser ,id=id)
        followers = FollowAndFollowingModel.objects.filter(friend_by=user)
        return Response(FollowAndFollowingModelSerializer(followers,many=True).data, status=status.HTTP_200_OK)
    
    def post(self,request,id):
        user=get_object_or_404(CustomUser,id = id)
        friend=FollowAndFollowingModel.objects.filter(my_by=request.user, friend_by=user).exists()
        if friend:
            chat=get_object_or_404(FollowAndFollowingModel,my_by=request.user,friend_by=user)
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
    permission_classes = (permissions.IsAuthenticated,)
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
            if not NotificationModel.objects.filter(notification_visible_to_user = user, \
                                                following_user = user).exists():
                notification = NotificationModel.objects.create(
                                notification_visible_to_user = user,
                                following_user = request.user,
                                follow_or_like = 1
                    )
                notification.save()
            return Response(status=status.HTTP_201_CREATED)

class ProfileImageDeleteAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def delete(self,request,id):
        image_length = request.user.image.all()
        if len(image_length) >1 and id!=17:
            image = get_object_or_404(ProfileImage,id = id)
            image.delete()
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'data':'You can not this photo.Becouse first photo left in profile'},status=status.HTTP_200_OK)


class ProfileImageAllAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        user = get_object_or_404(CustomUser,id=id).image.all()
        return Response(ProfileImageSerializer(user,many=True).data,status=status.HTTP_200_OK)

class OfferFriendToUserAPiView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        friends = FollowAndFollowingModel.objects.filter(my_by=request.user).values_list('friend_by',flat=True)
        friends_list = list(friends)
        friends_list.append(request.user.id)
        suggest_user= CustomUser.objects.filter(
            ~Q(id__in=friends_list),
        )
        return Response(ProfileSerializer(suggest_user,many=True).data,status=status.HTTP_200_OK)
class UserListApiView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        users = CustomUser.objects.filter(~Q(id=request.user.id))
        return Response(ProfileSerializer(users,many=True).data,status=status.HTTP_200_OK)
        

class FollowingAndFollowersCountApiViews(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,id):
        following = FollowAndFollowingModel.objects.filter(my_by__id = id).count()
        followers = FollowAndFollowingModel.objects.filter(friend_by__id = id).count()
        return Response({"following":following,"followers":followers},status=status.HTTP_200_OK)

# class CurrentUserView(views.APIView):
#     permission_classes = [permissions.IsAuthenticated, PaidServicePermission]

#     def get(self, request):
#         serializer = UserSerializer(request.user)
#         return response.Response(serializer.data)

#     def get_object(self, queryset=None):
#         return self.request.user

#     def post(self, request):
#         self.object = self.get_object()
#         serializer = UserPasswordChangeSerializer(data=request.data)
#         user_info_serializer = UserSerializer(request.user)
#         if serializer.is_valid():
#             # Check old password
#             old_password = serializer.data.get("old_password")
#             if not self.object.check_password(old_password):
#                 return response.Response(
#                     {
#                         "old_password": ["Wrong password."]
#                      },
#                     status=status.HTTP_400_BAD_REQUEST)
#             # set_password also hashes the password that the user will get
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             return response.Response(user_info_serializer.data, status=status.HTTP_200_OK)

#         return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
