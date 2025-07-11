from rest_framework import serializers

from ..models import Conversation, Message
from ..models.chat_setting import ChatSetting


# 定義　response model
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']
        read_only_fields = ['id', 'timestamp']


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'messages']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class UserMessageSerializer(serializers.Serializer):
    # 直接與 model　綁定
    message = serializers.CharField(required=True)

class ChatSettingSerializer(serializers.Serializer):
    class Mata:
        model = ChatSetting
        fields = ['reply_style', 'tone', 'model', 'pre_constructed_prompt','created_at', 'updated_at', 'api_key']
