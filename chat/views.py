
from django.shortcuts import render
from rest_framework import views,serializers,permissions,response,status
from django.shortcuts import get_object_or_404

from chat.serializers import ChatGetSerializer,ChatPostSerializer
from .models import ChatModel,CustomUser
import json
class ChatUserAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request,id):
        readby = get_object_or_404(CustomUser,id=id)
        writeby = request.user
        new1=ChatModel.objects.filter(write_by=writeby,read_by = readby ).order_by('-data')
        new2=ChatModel.objects.filter(write_by=readby,read_by = writeby ).order_by('-data')
        cos=list(new1)+list(new2)
        for i in cos:
            for j in cos:
                if i.data < j.data:
                    i.write_by, j.write_by = j.write_by, i.write_by
                    i.read_by, j.read_by = j.read_by, i.read_by
                    i.data, j.data = j.data, i.data
                    i.message, j.message = j.message, i.message
        return response.Response(ChatGetSerializer(cos,many=True).data,status=status.HTTP_200_OK)
    
    def post(self,request,id):
        get_message= ChatPostSerializer(data = request.data)
        readby = get_object_or_404(CustomUser,id=id)
        writeby = request.user
        print(request.data['message'])
        if get_message.is_valid():
            get_message.save(write_by = writeby,read_by = readby)
            return response.Response(status=status.HTTP_201_CREATED)
        else:
            print(get_message.errors)
            return response.Response({"error":get_message.errors},status=status.HTTP_400_BAD_REQUEST)

            

        



