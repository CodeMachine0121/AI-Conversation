from typing import Dict, Any
from openai import OpenAI

from playms_homework.conversations.models.chat_setting import ChatSetting


class AIProxy:
    def __init__(self, user_id: str):
        self.user_chat_setting = ChatSetting.objects.get(user_id=user_id)
        api_key = self.user_chat_setting.api_key
        self.client = OpenAI(api_key=api_key)

    def generate_response(self, user_message: str) -> str:

        pre_prompt = self.user_chat_setting.pre_constructed_prompt + "\n\n"  +  self.user_chat_setting.reply_style + "\n\n" +  self.user_chat_setting.tone

        response = self.client.responses.create(
            model= self.user_chat_setting.model,
            instructions= pre_prompt,
            input= user_message)

        return response.output_text
