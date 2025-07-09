from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..business_logic.services import ConversationService
from ..models import Conversation
from .serializers import ConversationSerializer, MessageSerializer, UserMessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = ConversationService()

    def get_queryset(self):
        """
        Get conversations for the current user.
        """
        return Conversation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new conversation for the current user.
        """
        return self.service.create_conversation(self.request.user.id)


    """
        Close a conversation.
    """
    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        conversation = self.service.close_conversation(pk)
        if not conversation:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_200_OK
        )

    """
        Reopen a closed conversation.
    """
    @action(detail=True, methods=['post'])
    def reopen(self, request, pk=None):
        conversation = self.service.reopen_conversation(pk)
        if not conversation:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_200_OK
        )

    """
        Get all messages for a conversation.
    """
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        messages = self.service.get_conversation_messages(pk)
        return Response(
            MessageSerializer(messages, many=True).data,
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """
        Send a message to the AI and get a response.
        """
        serializer = UserMessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user_message = serializer.validated_data['message']
        ai_message = self.service.generate_ai_response(pk, user_message)

        if not ai_message:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            MessageSerializer(ai_message).data,
            status=status.HTTP_201_CREATED
        )
