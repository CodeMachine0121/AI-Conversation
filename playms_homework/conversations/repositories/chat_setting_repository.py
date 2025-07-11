"""ChatSettingRepository 模組，提供 ChatSetting 的資料存取方法。"""

from typing import Any, Dict
from playms_homework.conversations.models.chat_setting import ChatSetting


class ChatSettingRepository:
    """Repository for ChatSetting model."""

    @staticmethod
    def create_chat_setting(user_id: str, settings_data: Dict[str, Any]) -> ChatSetting:
        """
        建立新的 ChatSetting。
        :param user_id: 使用者 ID
        :param settings_data: 設定資料
        :return: 新建立的 ChatSetting 物件
        """
        # pylint: disable=no-member

        chat_setting = ChatSetting.objects.create(
            user_id=user_id,
            **settings_data
        )
        return chat_setting

    @staticmethod
    def update_chat_setting(user_id: str, settings_data: Dict[str, Any]) -> ChatSetting:
        """
        更新指定使用者的 ChatSetting。
        :param user_id: 使用者 ID
        :param settings_data: 設定資料
        :return: 更新後的 ChatSetting 物件
        """
        # pylint: disable=no-member
        chat_setting = ChatSetting.objects.get(user_id=user_id)
        for key, value in settings_data.items():
            setattr(chat_setting, key, value)
        chat_setting.save()
        return chat_setting

    @staticmethod
    def get_chat_setting(user_id: str) -> ChatSetting:
        """
        取得指定使用者的 ChatSetting。
        :param user_id: 使用者 ID
        :return: ChatSetting 物件
        """
        # pylint: disable=no-member
        return ChatSetting.objects.get(user_id=user_id)
