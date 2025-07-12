"""ChatSettingViewSet 模組，提供 ChatSetting 的 API 介面。"""
from typing import Dict, Any

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

    def list(self, request):
        """
        取得目前使用者的 ChatSetting。
        對應 GET /api/chat-setting/ 請求
        """
        try:
            chat_setting = self.service.get_chat_setting(request.user.id)
            data = ChatSettingSerializer(chat_setting).data
            return Response(
                data= data,
                status=status.HTTP_200_OK
            )
        except Exception:
            # 如果用戶還沒有設定，返回 404
            return Response(
                {"detail": "No settings found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def create(self, request):
        """
        建立或更新目前使用者的 ChatSetting。
        對應 POST /api/chat-setting/ 請求
        """
        user_id = request.user.id
        chat_setting = self.service.upsert_chat_setting(
            user_id= user_id,
            settings_data= request.initial_data)

        return Response(
            ChatSettingSerializer(chat_setting).data,
            status=status.HTTP_201_CREATED
        )
