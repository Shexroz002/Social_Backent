from django.db import models
from users.models import CustomUser

# Create your models here.

class ChatModel(models.Model):
    write_by = models.ForeignKey(CustomUser,verbose_name='Yozgan Foydalanuvchi:',on_delete=models.CASCADE,related_name='write_by')
    read_by = models.ForeignKey(CustomUser,verbose_name='Oqigan  Foydalanuvchi:',on_delete=models.CASCADE,related_name='read_by')
    message = models.CharField(max_length=250,null=False,blank=False)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.write_by.username
