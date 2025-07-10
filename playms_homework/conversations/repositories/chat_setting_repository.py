from playms_homework.conversations.models.chat_setting import ChatSetting


class ChatSettingRepository:

    @staticmethod
    def create_chat_setting(settings_data: ChatSetting) -> ChatSetting:
            """
            Create a new conversation for a user.

            Args:
                user_id: The ID of the user.

            Returns:
                The newly created conversation.
            """
            return ChatSetting.objects.create(user_id=settings_data.user_id)
