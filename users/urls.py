from django.urls import path,re_path
from .views import RegisterView,ProfileupdataView,\
                ProfileImageDeleteAPIView,FollowersAPIView,\
                FollowingAPIView,OfferFriendToUserAPiView,\
                ProfileImageAllAPIView,UserListApiView,FollowingAndFollowersCountApiViews
from rest_framework.authtoken import views as auth_views


app_name = 'users'
urlpatterns =[
    path('api/register',RegisterView.as_view(),name='register'),
    path('api/user/profile/image/delete/<int:id>',ProfileImageDeleteAPIView.as_view(),name='deleteimage'),
    path('api/user/profile/image/<int:id>',ProfileImageAllAPIView.as_view(),name='deleteimage'),
    path('api/followers/<int:id>',FollowersAPIView.as_view()),
    path('api/suggest',OfferFriendToUserAPiView.as_view()),
    path('api/following/<int:id>',FollowingAPIView.as_view()),
    path('api/profile/update/<int:pk>',ProfileupdataView.as_view()),
    path('api/user/list',UserListApiView.as_view(),name='userlist'),
    path('follow/and/followers/count/<int:id>',FollowingAndFollowersCountApiViews.as_view(),name='follow'),
    re_path(r'^auth/$', auth_views.obtain_auth_token,name='login')
]