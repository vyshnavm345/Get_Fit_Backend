from django.db import models
# from django.conf import settings
from user.models import UserAccount

class ChatMessage(models.Model):
    room_name = models.CharField(max_length=255)
    sender = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.sender.fullname()}: {self.message[:20]}" 