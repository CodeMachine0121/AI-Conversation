from abc import abstractmethod, ABC
from typing import List

from openai import OpenAI

from playms_homework.conversations.models import Message
from playms_homework.conversations.models.chat_setting import ChatSetting


class AiProxyInterface(ABC):
    @abstractmethod
    def generate_response(self, user_chat_setting: ChatSetting, conversation_messages: List[Message]) -> str:
        pass


class OpenAiProxy(AiProxyInterface):

    def generate_response(self, user_chat_setting: ChatSetting, conversation_messages: List[Message]) -> str:

        client = OpenAI(api_key=user_chat_setting.api_key)
        pre_prompt = user_chat_setting.pre_constructed_prompt + "\n\n"  +  user_chat_setting.reply_style + "\n\n" +  user_chat_setting.tone

        messages = [{"role": "system", "content": pre_prompt}]

        # 将 conversation_messages 转换为 OpenAI API 格式
        for message in conversation_messages:
            if message.sender == 'user':
                messages.append({"role": "user", "content": message.content})
            elif message.sender == 'ai':
                messages.append({"role": "assistant", "content": message.content})

        completion = client.chat.completions.create(
            model=user_chat_setting.model,
            messages=messages,
        )

        response_content = completion.choices[0].message.content
        return response_content
