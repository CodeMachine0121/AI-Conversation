from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import action
from django.contrib.auth import get_user_model

from ..models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

User = get_user_model()

class ConversationManagementViewSet(ViewSet):
    """
    Admin-only viewset for managing all conversations
    """
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    def list(self, request):
        """
        List all conversations for admin users
        """
        conversations = Conversation.objects.select_related('user').order_by('-updated_at')

        # 支援按用戶篩選
        user_param = request.query_params.get('user', None)
        if user_param:
            conversations = conversations.filter(user__username=user_param)

        # 支援按狀態篩選
        status_param = request.query_params.get('status', None)
        if status_param:
            conversations = conversations.filter(status=status_param)

        # 支援搜索
        search_param = request.query_params.get('search', None)
        if search_param:
            conversations = conversations.filter(
                user__username__icontains=search_param
            )

        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Get a specific conversation details
        """
        try:
            conversation = Conversation.objects.select_related('user').get(pk=pk)
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Get all messages for a specific conversation
        """
        try:
            conversation = Conversation.objects.get(pk=pk)
            messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """
        Close a conversation (admin action)
        """
        try:
            conversation = Conversation.objects.get(pk=pk)
            conversation.status = 'closed'
            conversation.save()
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['post'])
    def reopen(self, request, pk=None):
        """
        Reopen a conversation (admin action)
        """
        try:
            conversation = Conversation.objects.get(pk=pk)
            conversation.status = 'active'
            conversation.save()
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )
