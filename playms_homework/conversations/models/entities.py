from django.db import models
from django.conf import settings

class Conversation(models.Model):
    """
    Model to store conversation sessions between users and the AI.
    """
    ACTIVE = 'active'
    CLOSED = 'closed'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (CLOSED, 'Closed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation {self.id} - {self.user.username}"


class Message(models.Model):
    """
    Model to store individual messages within a conversation.
    """
    USER = 'user'
    AI = 'ai'
    SENDER_CHOICES = [
        (USER, 'User'),
        (AI, 'AI'),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=4, choices=SENDER_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} message in conversation {self.conversation.id}"
