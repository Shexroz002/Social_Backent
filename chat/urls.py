from django.urls import path
from .views import ChatUserAPIView

urlpatterns=[
    path('api/chat/<int:id>',ChatUserAPIView.as_view())
]