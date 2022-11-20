from django.urls import path
from .views import \
            FavoritePostAllApiViews, FavoritePostDetailApiViews, PostCreateAPIViews,PostDetailApiViews,\
            PostLikeApiViews,StoryApiViews,\
            CommentsAPIviews,NotificationAPIView,\
            StoryIsSeenByUserAPIView,PeronalStoryAPIView,\
            CommentsDeleteAPIviews,ReadedPostApiView,ReadingPostApiView,ReadPostApiView
app_name = 'feed'

urlpatterns = [
    path('api/post',PostCreateAPIViews.as_view(),name='feeds'),# passed test
    path('api/post/<int:id>',PostDetailApiViews.as_view(),name='detail'),# passed test
    path('api/post/comments/<int:id>',CommentsAPIviews.as_view(),name='comments'),# passed test
    path('api/post/comments/delete/<int:id>',CommentsDeleteAPIviews.as_view(),name='comment_detail'),# passed test
    path('api/post/like/<int:id>',PostLikeApiViews.as_view(),name='like'),# passed test
    path('api/story',StoryApiViews.as_view(),name='story'),# passed test
    path('api/story/seen/<int:id>',StoryIsSeenByUserAPIView.as_view(),name = 'seen_story'),# passed test
    path('api/story/seen/personal/<int:id>',PeronalStoryAPIView.as_view(),name = 'personal_story'),# passed test
    path('api/notifications',NotificationAPIView.as_view(),name = 'notifications'),# passed test
    path('api/favorite/post/all',FavoritePostAllApiViews.as_view(),name = 'favorite_all'),# passed test
    path('api/favorite/post/<int:id>',FavoritePostDetailApiViews.as_view(),name = 'favorite_detail'),# passed test
    path('api/readed/book/<int:id>',ReadedPostApiView.as_view(),name = 'readed_book'),
    path('api/reading/book',ReadingPostApiView.as_view(),name = 'reading_book'),
    path('api/read/book',ReadPostApiView.as_view(),name = 'readeds_book'),
]
