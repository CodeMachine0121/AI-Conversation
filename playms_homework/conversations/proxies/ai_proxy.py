from typing import Dict, Any
from openai import OpenAI

from playms_homework.conversations.models.chat_setting import ChatSetting


class AIProxy:

    @staticmethod
    def generate_response(user_message: str, user_chat_setting: ChatSetting) -> str:

        client = OpenAI(api_key=user_chat_setting.api_key)
        pre_prompt = user_chat_setting.pre_constructed_prompt + "\n\n"  +  user_chat_setting.reply_style + "\n\n" +  user_chat_setting.tone

        response = client.responses.create(
            model= user_chat_setting.model,
            instructions= pre_prompt,
            input= user_message)

        return response.output_text
