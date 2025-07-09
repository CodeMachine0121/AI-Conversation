from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    """
    Inline admin for messages within a conversation.
    """
    model = Message
    readonly_fields = ['sender', 'content', 'timestamp']
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """
    Admin for conversations.
    """
    list_display = ['id', 'user_link', 'status', 'created_at', 'updated_at', 'message_count']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['user', 'created_at', 'updated_at']
    inlines = [MessageInline]

    def user_link(self, obj):
        """
        Return a link to the user admin page.
        """
        url = reverse("admin:users_user_change", args=[obj.user.id])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'

    def message_count(self, obj):
        """
        Return the number of messages in the conversation.
        """
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin for messages.
    """
    list_display = ['id', 'conversation_link', 'sender', 'content_preview', 'timestamp']
    list_filter = ['sender', 'timestamp']
    search_fields = ['content', 'conversation__user__username']
    readonly_fields = ['conversation', 'sender', 'content', 'timestamp']

    def conversation_link(self, obj):
        """
        Return a link to the conversation admin page.
        """
        url = reverse("admin:conversations_conversation_change", args=[obj.conversation.id])
        return format_html('<a href="{}">{}</a>', url, obj.conversation.id)
    conversation_link.short_description = 'Conversation'

    def content_preview(self, obj):
        """
        Return a preview of the message content.
        """
        max_length = 50
        if len(obj.content) > max_length:
            return obj.content[:max_length] + '...'
        return obj.content
    content_preview.short_description = 'Content'

    def has_add_permission(self, request):
        return False
