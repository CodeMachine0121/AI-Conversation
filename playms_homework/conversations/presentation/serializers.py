from rest_framework import serializers

from ..models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    """

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    """
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'messages']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class UserMessageSerializer(serializers.Serializer):
    """
    Serializer for user messages.
    """
    message = serializers.CharField(required=True)
