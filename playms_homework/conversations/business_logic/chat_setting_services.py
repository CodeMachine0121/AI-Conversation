"""ChatSettingService 模組，提供 ChatSetting 的商業邏輯。"""

from typing import Any, Dict
from playms_homework.conversations.models.chat_setting import ChatSetting
from playms_homework.conversations.repositories.chat_setting_repository import ChatSettingRepository


class ChatSettingService:
    """Service for ChatSetting business logic."""

    def __init__(self):
        """
        初始化 ChatSettingService，建立 repository 實例。
        """
        self.repository = ChatSettingRepository()

    def upsert_chat_setting(self, user_id: str, settings_data: Dict[str, Any]) -> ChatSetting:
        """
        建立/更新 ChatSetting。
        :param user_id: 使用者 ID
        :param settings_data: 設定資料
        :return: ChatSetting 物件
        """
        if self.repository.is_user_chat_setting_exists(user_id):
            return self.repository.update_chat_setting(user_id, settings_data)

        return self.repository.create_chat_setting(user_id, settings_data)

    def get_chat_setting(self, user_id: str) -> ChatSetting:
        """
        取得指定使用者的 ChatSetting。
        :param user_id: 使用者 ID
        :return: ChatSetting 物件
        """
        return self.repository.get_chat_setting(user_id)
