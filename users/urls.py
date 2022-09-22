from django.urls import path,re_path
from .views import RegisterView,ProfileupdataView,ProfileImageDeleteAPIView,FollowersAPIView,FollowingAPIView
from rest_framework.authtoken import views as auth_views

urlpatterns =[
    path('api/register',RegisterView.as_view(),name='register'),
    path('api/user/profile/image/delete/<int:id>',ProfileImageDeleteAPIView.as_view(),name='deleteimage'),
    path('api/followers/<int:id>',FollowersAPIView.as_view()),
    path('api/following/<int:id>',FollowingAPIView.as_view()),
    path('api/profile/update/<int:pk>',ProfileupdataView.as_view()),
    re_path(r'^auth/$', auth_views.obtain_auth_token)
]