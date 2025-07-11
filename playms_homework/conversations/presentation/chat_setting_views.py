"""ChatSettingViewSet 模組，提供 ChatSetting 的 API 介面。"""

from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from playms_homework.conversations.business_logic.chat_setting_services import ChatSettingService
from playms_homework.conversations.presentation.serializers import ChatSettingSerializer


class ChatSettingViewSet(viewsets.ModelViewSet):
    """ViewSet for ChatSetting."""
    serializer_class = ChatSettingSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self, *args, **kwargs):
        """
        初始化 ChatSettingViewSet，建立 service 實例。
        """
        super().__init__(**kwargs)
        self.service = ChatSettingService()

    def get_chat_settings(self, request):
        """
        取得目前使用者的 ChatSetting。
        :param request: 請求物件
        :return: Response
        """
        chat_setting = self.service.get_chat_setting(request.user.id)
        return Response(
            ChatSettingSerializer(chat_setting).data,
            status=status.HTTP_200_OK
        )

    def perform_create(self, serializer):
        """
        建立目前使用者的 ChatSetting。
        :param serializer: serializer 實例
        :return: Response
        """
        user_id = self.request.user.id
        chat_setting = self.service.create_chat_setting(user_id=user_id, settings_data=serializer.validated_data)
        return Response(
            ChatSettingSerializer(chat_setting).data,
            status=status.HTTP_201_CREATED
        )

    def update_chat_settings(self, request):
        """
        更新目前使用者的 ChatSetting。
        :param request: 請求物件
        :return: Response
        """
        serializer = ChatSettingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        user_id = request.user.id
        chat_setting = self.service.update_chat_setting(user_id, serializer.validated_data)
        return Response(
            ChatSettingSerializer(chat_setting).data,
            status=status.HTTP_200_OK
        )
