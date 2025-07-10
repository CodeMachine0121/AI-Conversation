from playms_homework.conversations.models.chat_setting import ChatSetting
from playms_homework.conversations.repositories.chat_setting_repository import ChatSettingRepository

class ChatSettingService:
    def __init__(self):
        self.repository = ChatSettingRepository()
    def create_chat_setting(self, settings_data: ChatSetting) -> dict:
        """
        Create a new chat setting for a user.

        Args:
            user_id: The ID of the user.
            settings_data: A dictionary containing the settings data.

        Returns:
            The newly created chat setting.
        """
        return self.repository.create_chat_setting( settings_data)
