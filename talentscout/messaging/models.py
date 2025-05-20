from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()
class Conversation(models.Model):
    participants = models.ManyToManyField(User)
    started_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    conversation = models.ForeignKey('Conversation', on_delete=models.CASCADE, null=False, blank=False)


    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"

    class Meta:
        ordering = ['timestamp']
    

