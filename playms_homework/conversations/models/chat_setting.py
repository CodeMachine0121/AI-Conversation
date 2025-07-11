from django.db import models
from django.conf import settings

class ChatSetting(models.Model):
    """
    Model to store conversation sessions between users and the AI.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_settings')
    reply_style = models.CharField(max_length=100, default='default_style')
    tone = models.CharField(max_length=50, default='neutral')
    model = models.CharField(max_length=50, default='gpt-4o')
    pre_constructed_prompt = models.TextField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    api_key = models.CharField(max_length=255, blank=True, null=True, default=None)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"chat setting {self.id} - {self.user.username}"
