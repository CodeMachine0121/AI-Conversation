from requests.models import Response

from playms_homework.conversations.business_logic.setting_services import SettingService
from playms_homework.conversations.presentation.serializers import ConversationSerializer
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated


class SettingViewSet(viewsets.ModelViewSet):

    serializer_class = ConversationSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = SettingService()
    """
    ViewSet for handling settings-related operations.
    """

    def get_settings(self, request):
        """
        Retrieve the current settings.
        """
        # Logic to retrieve settings
        return Response(
            status=status.HTTP_200_OK
        )

    def create_settings(self, request):
        """
        Create new settings based on the provided request data.
        :param request:
        :return:
        """


    def update_settings(self, request):
        """
        Update the settings with provided data.
        """
        # Logic to update settings
        return {"status": "settings updated"}
