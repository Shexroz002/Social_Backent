from tkinter import PhotoImage
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser,ProfileImage

class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ('id','photo')
        extra_kwargs = {
            'photo': {'required': False}
        }
    
    def create(self, validated_data):
        photo = ProfileImage.objects.create(
            photo = validated_data['photo']
        )
        
        photo.save()
        return photo
    


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ('id','username', 'password','email','last_name','first_name')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
            'email': {'required': False},
            'last_name': {'required': False},
            'first_name': {'required': False},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username = validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    image = ProfileImageSerializer(many=True,read_only=True)
    class Meta:
        model = CustomUser
        fields = ('id','username','email','last_name','first_name','image')
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'last_name': {'required': False},
            'first_name': {'required': False},
            'image': {'required': False},
            'password':{'required':False}
        }

    def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)
            instance.email = validated_data.get('email', instance.email)
            instance.last_name = validated_data.get('last_name', instance.last_name)
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.save()
            return instance


class FollowAndFollowingModelSerializer(serializers.ModelSerializer):
    my_by = ProfileSerializer(read_only=True)
    friend_by = ProfileSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = ('id','friend_by','my_by')
