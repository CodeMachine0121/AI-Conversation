from playms_homework.conversations.business_logic.chat_setting_services import ChatSettingService
from playms_homework.conversations.presentation.serializers import ConversationSerializer, ChatSettingSerializer
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

class ChatSettingViewSet(viewsets.ModelViewSet):

    serializer_class = ConversationSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = ChatSettingService()
    """
    ViewSet for handling settings-related operations.
    """

    def get_chat_settings(self, request):
        """
        Retrieve the current settings.
        """
        # Logic to retrieve settings
        return Response(
            status=status.HTTP_200_OK
        )


    def perform_create(self, request):
        """
        Create new settings based on the provided request data.
        """
        serializer = ChatSettingSerializer(data=request.data)
        if serializer.is_valid():
            settings_data = serializer.validated_data
            user_id = self.request.user.id
            chat_setting = self.service.create_chat_setting(user_id, settings_data)
            return Response(
                ChatSettingSerializer(chat_setting).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



    def update_chat_settings(self, request):
        """
        Update the settings with provided data.
        """
        # Logic to update settings
        return {"status": "settings updated"}
