from http import client
from rest_framework import permissions
from rest_framework import status
from rest_framework import response
from rest_framework import views
from django.shortcuts import get_object_or_404
from django.db.models import *
from users.models import CustomUser, FollowAndFollowingModel
from .models import NotificationModel, PostModel, StoryModel,CommentModel,FavoritePosts,ReadedPost,BookType
from .serializers import \
                        PostSerialzier,StorySerializer,ReadedPostSerializer,\
                        CommentSerializer,NotificationsSerializers , FavoritePostSerializer,\
                        BookTypeSerializer
            
                        
# Create your views here.

class PostCreateAPIViews(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        friend=FollowAndFollowingModel.objects.filter(my_by=request.user)
        if friend:
            book=list()
            for i in friend:
                book+=list(PostModel.objects.filter(post_creator=i.friend_by).order_by('-create_by')[:2])
            for i in range(0,len(book)):
                for j in range(i+1,len(book)):
                    if book[i].create_by <= book[j].create_by:
                        book[i],book[j]=book[j],book[i]

                    elif book[i].create_by == book[j].create_by:
                        if book[i].like.count()+ book[i].comment_count <= \
                                                            book[j].like.count()+ book[i].comment_count:
                            book[i], book[j] = book[j], book[i]
                        else:
                            book[i]=book[i]
                            book[j]=book[j]
                    else:
                        book[i] = book[i]
                        book[j] = book[j]
        else:
            book=list(PostModel.objects.all())
            for i in range(0,len(book)):
                for j in range(i+1,len(book)):
                    if book[i].like.count() + book[i].comment_count <= \
                                                           book[j].like.count()+ book[i].comment_count:
                        book[i],book[j]=book[j],book[i]
                    elif book[i].like.count() + book[i].comment_count == \
                                                            book[j].like.count() + book[i].comment_count:
                        if book[i].date <= book[j].date:
                            book[i],book[j]=book[j],book[i]


                        else:
                            book[i]=book[i]
                            book[j]=book[j]
                    else:
                        book[i] = book[i]
                        book[j] = book[j]
        best_book = list(PostModel.objects.all())
        for i in range(0,len(best_book)):
                for j in range(i+1,len(best_book)):
                    if best_book[i].like.count() +best_book[i].comment_count <= \
                                                best_book[j].like.count() + best_book[i].comment_count:
                        best_book[i],best_book[j]=best_book[j],best_book[i]
        for i in best_book[:3]:
                if i not in book:
                    book.append(i)
        like_count = list()
        book_type = BookType.objects.all()
        for i in book_type:
            count =  NotificationModel.objects.filter(notification_visible_to_user=request.user,\
                follow_or_like=0,post_like__post_type__book_type=i.book_type
            ).count()
            book_count=[i.book_type,count]
            like_count.append(book_count)
        for i in range(1,len(like_count)):
            if like_count[0][1]<like_count[i][1]:
                like_count[0],like_count[i]=like_count[i],like_count[0]
        for type in like_count[:4]:
            book_type = get_object_or_404(BookType,book_type=type[0])
            type_book = list(PostModel.objects.filter(post_type = book_type))          
            for i in range(0,len(type_book)):
                for j in range(i+1,len(type_book)):
                    if type_book[i].like.count() +type_book[i].comment_count <= \
                                                type_book[j].like.count() + type_book[i].comment_count:
                        type_book[i],type_book[j]=type_book[j],type_book[i]
            for i in type_book[:3]:
                if i not in book:
                    book.append(i)
            
        return response.Response(PostSerialzier(tuple(book),many=True).data,status = status.HTTP_200_OK)

    def post(self,request):
        serializer = PostSerialzier(data = request.data)
        if serializer.is_valid():
            print(request.data)
            type = get_object_or_404(BookType,book_type=request.data.get('post_type'))
            post_deetail = serializer.save()
            post_deetail.post_creator = request.user
            post_deetail.post_type = type
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
                post_upadate = serializer_feed.save()
                if(request.data.get('post_image')):
                    post_upadate.post_image = request.data.get('post_image')
                    post_upadate.save()
                return response.Response(PostSerialzier(post_upadate).data,status=status.HTTP_201_CREATED)
            else:
                return response.Response(
                    {
                    'error':'You can not update this post.\
                    Becouse, You did not create this post.'
                    },\
                    status=status.HTTP_400_BAD_REQUEST)
        else:
            print(serializer_feed.errors)
            return response.Response({'error':serializer_feed.errors},status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,id):
        feed = get_object_or_404(PostModel,id=id)
        if feed.post_creator == request.user:
            feed.delete()
            return response.Response({'state':False},status=status.HTTP_404_NOT_FOUND)
        else:
                return response.Response({'error':'You can not delete this post.\
                                Becouse, You did not create this post.'},status=status.HTTP_400_BAD_REQUEST)


class PostLikeApiViews(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        feed = get_object_or_404(PostModel,id=id)
        post = feed.like.all()
        user = request.user
        if user in post:
            feed.like.remove(user)
            feed.save()
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        else:
            if not NotificationModel.objects.filter(notification_visible_to_user = user, \
                                                post_like = feed).exists():
                notification = NotificationModel.objects.create(
                                notification_visible_to_user = feed.post_creator,
                                following_user = request.user,
                                post_like = feed,
                                follow_or_like = 0
                    )
                notification.save()
            feed.like.add(user)
            feed.save()
            return response.Response(status=status.HTTP_201_CREATED)


class StoryIsSeenByUserAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        post = get_object_or_404(StoryModel,id=id)
        post_model = post.seen_user.all()
        user = request.user
        if  user in post_model:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            post.seen_user.add(user)
            post.save()
            return response.Response(status=status.HTTP_200_OK)


class PeronalStoryAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        user = get_object_or_404(CustomUser,id=id)
        story = StoryModel.objects.filter(story_creator=user).last()
        return response.Response(StorySerializer(story).data,status=status.HTTP_200_OK)

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
        post_serialier = PostSerialzier(post)
        comments = CommentModel.objects.filter(feed_by = post).order_by('date_by')
        return response.Response(
            {'comments':CommentSerializer(comments,many=True).data,
            'post_data':post_serialier.data
            },
        status = status.HTTP_200_OK)

    def post(self,request,id):
        post = get_object_or_404(PostModel,id=id)
        user = request.user
        seriazliers = CommentSerializer(data = request.data)
        if seriazliers.is_valid():
            new_comment = seriazliers.save()
            new_comment.create_by=user
            new_comment.feed_by=post
            new_comment.save()
            post.comment_count += 1
            post.save()
            return response.Response(CommentSerializer(new_comment).data,status=status.HTTP_201_CREATED)
        else:
            return response.Response({'eror':seriazliers.errors},status=status.HTTP_400_BAD_REQUEST)

class CommentsDeleteAPIviews(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self,request,id):
        comments = get_object_or_404(CommentModel,id=id)
        return response.Response(CommentSerializer(comments).data,status = status.HTTP_200_OK)

    def delete(self,request,id):
        comments = get_object_or_404(CommentModel,id=id)
        comments.delete()
        return response.Response(status = status.HTTP_404_NOT_FOUND)

    def put(self,request,id):
        data = request.data.get('comment')
        comments = get_object_or_404(CommentModel,id=id)
        comments.comment=data
        comments.save()
        return response.Response(CommentSerializer(comments).data,status = status.HTTP_201_CREATED)


class NotificationAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        notifications = NotificationModel.objects.filter(
                                                notification_visible_to_user = request.user).order_by('-date')
        return response.Response(NotificationsSerializers(notifications,many = True).data,
                                                                status=status.HTTP_200_OK)
class FavoritePostDetailApiViews(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request,id):
        post = get_object_or_404(PostModel,id = id)
        favorite_post_status = FavoritePosts.objects.filter(client = request.user,favorite_post = post).exists()
        if not favorite_post_status:
            favorite_post = FavoritePosts.objects.create(
                            client = request.user,
                            favorite_post = post
            ).save()
            return response.Response(status=status.HTTP_201_CREATED)
        else:
            return response.Response(status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,id):
        post = get_object_or_404(PostModel,id = id)
        favorite_post_delete = FavoritePosts.objects.filter(favorite_post = post, client = request.user).last()
        favorite_post_delete.delete()
        return response.Response(status = status.HTTP_404_NOT_FOUND)


class FavoritePostAllApiViews(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self,request):
        favorite_post = FavoritePosts.objects.filter(client = request.user)
        return response.Response(FavoritePostSerializer(favorite_post,many=True).data,\
                                                            status=status.HTTP_200_OK)       

class ReadedPostApiView(views.APIView):
    def get(self,request,id):
        post = get_object_or_404(PostModel,id=id)
        if ReadedPost.objects.filter(client = request.user,post= post).exists():
            return response.Response({'info':'This book has been added to the books to read'},status = status.HTTP_404_NOT_FOUND)
        book_to_read = ReadedPost.objects.create(client = request.user,post= post).save()
        return response.Response({'info':'This book was added successfully to the books to read',"data":PostSerialzier(book_to_read).data},status=status.HTTP_200_OK)
    
    def post(self,request,id):
        print('id',id)
        post = get_object_or_404(PostModel,id=id)
        if ReadedPost.objects.filter(client = request.user,post= post,status=False).exists():
            readed_book = ReadedPost.objects.get(client = request.user,post= post,status=False)
            readed_book.status = True
            readed_book.save()
            return response.Response(ReadedPostSerializer(readed_book).data,\
                                        status = status.HTTP_201_CREATED)

        return response.Response({'info':'This book isnt contain'},\
                                    status=status.HTTP_400_BAD_REQUEST
            )
    def delete(self,request,id):
        post = get_object_or_404(PostModel,id=id)
        if ReadedPost.objects.filter(client = request.user,post= post).exists():
            book_to_read = ReadedPost.objects.filter(client = request.user,post= post)
            book_to_read.delete()
            return response.Response({'info':'This book has been deleted'},status = status.HTTP_404_NOT_FOUND)
        
        return response.Response({'info':'Not found'},status=status.HTTP_400_BAD_REQUEST)


class ReadingPostApiView(views.APIView):
    def get(self,request):
        read_posts = ReadedPost.objects.filter(client = request.user,status=False)
        return response.Response(ReadedPostSerializer(read_posts,many=True).data,status=status.HTTP_200_OK)

class ReadPostApiView(views.APIView):
    def get(self,request):
        read_posts = ReadedPost.objects.filter(client = request.user,status=True)
        return response.Response(ReadedPostSerializer(read_posts,many=True).data,status=status.HTTP_200_OK)

class BookTypeApiView(views.APIView):
    def get(self,request):
        book_type = BookType.objects.all()
        return response.Response(BookTypeSerializer(book_type,many=True).data,status=status.HTTP_200_OK)
        
