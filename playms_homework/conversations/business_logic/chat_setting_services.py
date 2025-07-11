from playms_homework.conversations.models.chat_setting import ChatSetting
from playms_homework.conversations.repositories.chat_setting_repository import ChatSettingRepository

class ChatSettingService:
    def __init__(self):
        self.repository = ChatSettingRepository()

    def create_chat_setting(self, user_id: str, settings_data: ChatSetting) -> ChatSetting:
        return self.repository.create_chat_setting(user_id, settings_data)

    def get_chat_settting(self, user_id) -> ChatSetting:
        return self.repository.get_chat_setting(user_id)

    def update_chat_setting(self, user_id, settings_data):
        self.repository.update_chat_setting(user_id, settings_data)
