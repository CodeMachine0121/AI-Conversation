from playms_homework.conversations.models.chat_setting import ChatSetting


class ChatSettingRepository:

    @staticmethod
    def create_chat_setting(user_id: str, settings_data: ChatSetting) -> ChatSetting:
            chat_setting = ChatSetting.objects.create(
                user_id=user_id,
                **settings_data
            )
            return chat_setting

    @staticmethod
    def get_chat_setting(user_id) -> ChatSetting:
        return ChatSetting.objects.get(user_id=user_id)

    @staticmethod
    def update_chat_setting(user_id, settings_data):
        chat_setting = ChatSetting.objects.get(user_id=user_id)
        for key, value in settings_data.items():
            setattr(chat_setting, key, value)
        chat_setting.save()
        return chat_setting

