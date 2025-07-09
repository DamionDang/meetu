from django.db import models
from users.models import CustomUser

class ChatMessage(models.Model):
    room_name = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} 在 {self.room_name} 中说: {self.message[:20]}'
# Create your models here.
