from django.urls import path
from .views import PostCreateAPIViews,PostDetailApiViews,PostLikeApiViews,StoryApiViews,CommentsAPIviews


urlpatterns = [
    path('api/post',PostCreateAPIViews.as_view()),
    path('api/post/<int:id>',PostDetailApiViews.as_view()),
    path('api/post/comments/<int:id>',CommentsAPIviews.as_view()),
    path('api/post/like/<int:id>',PostLikeApiViews.as_view()),
    path('api/story',StoryApiViews.as_view()),
]
