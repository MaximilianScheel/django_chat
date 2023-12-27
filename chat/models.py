from django.conf import settings
from django.db import models
from django.db.models.fields import DateField
from datetime import date

# Create your models here.

class Message(models.Model):
    text = models.CharField(max_length=255)
    created_at = DateField(default=date.today)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='chat_messages_set', default=None, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_messages_set')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver_messages_set')
    
    
class Chat(models.Model):
    created_at = DateField(default=date.today)
    