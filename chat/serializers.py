from dataclasses import fields
from rest_framework import serializers
from users.serializers import ProfileSerializer
from .models import ChatModel
class ChatPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatModel
        fields = "__all__"
        extra_kwargs = {
            'write_by': {'required': False},
            'read_by': {'required': False}
        }

class ChatGetSerializer(serializers.ModelSerializer):
    read_by= ProfileSerializer()
    class Meta:
        model = ChatModel
        fields = "__all__"