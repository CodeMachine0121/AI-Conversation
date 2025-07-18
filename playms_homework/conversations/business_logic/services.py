from typing import List, Optional, Dict, Any

from ..repositories.chat_setting_repository import ChatSettingRepository
from ..repositories.repositories import ConversationRepository
from ..proxies.ai_proxy import OpenAiProxy
from ..models import Conversation, Message


class ConversationService:
    """
    Service for managing conversations.
    This class contains the business logic for conversation management.
    """

    def __init__(self):
        self.repository = ConversationRepository()
        self.chat_setting_repository = ChatSettingRepository()

    def get_conversation(self, conversation_id: int) -> Optional[Conversation]:
        """
        Get a conversation by ID.

        Args:
            conversation_id: The ID of the conversation to retrieve.

        Returns:
            The conversation if found, None otherwise.
        """
        return self.repository.get_conversation(conversation_id)

    def get_user_conversations(self, user_id: int) -> List[Conversation]:
        """
        Get all conversations for a user.

        Args:
            user_id: The ID of the user.

        Returns:
            A list of conversations for the user.
        """
        return self.repository.get_user_conversations(user_id)

    def create_conversation(self, user_id: int) -> Conversation:
        """
        Create a new conversation for a user.

        Args:
            user_id: The ID of the user.

        Returns:
            The newly created conversation.
        """
        return self.repository.create_conversation(user_id)

    def close_conversation(self, conversation_id: int) -> Optional[Conversation]:
        """
        Close a conversation.

        Args:
            conversation_id: The ID of the conversation to close.

        Returns:
            The updated conversation if found, None otherwise.
        """
        return self.repository.update_conversation_status(conversation_id, Conversation.CLOSED)

    def reopen_conversation(self, conversation_id: int) -> Optional[Conversation]:
        """
        Reopen a closed conversation.

        Args:
            conversation_id: The ID of the conversation to reopen.

        Returns:
            The updated conversation if found, None otherwise.
        """
        return self.repository.update_conversation_status(conversation_id, Conversation.ACTIVE)

    def add_user_message(self, conversation_id: int, content: str) -> Optional[Message]:
        """
        Add a user message to a conversation.

        Args:
            conversation_id: The ID of the conversation.
            content: The content of the message.

        Returns:
            The newly created message if the conversation exists, None otherwise.
        """
        return self.repository.add_message(conversation_id, Message.USER, content)

    def generate_ai_response(self, user_id: int,  conversation_id: int, user_message: str) -> Optional[Message]:
        """
        Generate an AI response to a user message and add it to the conversation.

        Args:
            conversation_id: The ID of the conversation.
            user_message: The message from the user.
            context: Optional context information for the AI.

        Returns:
            The newly created AI message if the conversation exists, None otherwise.
            :param user_message:
            :param conversation_id:
            :param user_id:
        """
        # First, add the user message to the conversation
        user_message_obj = self.add_user_message(conversation_id, user_message)
        if not user_message_obj:
            return None


        # Generate AI response
        open_ai_proxy = OpenAiProxy()
        ai_response = open_ai_proxy.generate_response(
            user_chat_setting = self.chat_setting_repository.get_chat_setting(user_id),
            conversation_messages = self.repository.get_conversation_messages(conversation_id=conversation_id)
        )

        # Add AI response to the conversation
        return self.repository.add_message(conversation_id, Message.AI, ai_response)

    def get_conversation_messages(self, conversation_id: int) -> List[Message]:
        """
        Get all messages for a conversation.

        Args:
            conversation_id: The ID of the conversation.

        Returns:
            A list of messages for the conversation.
        """
        return self.repository.get_conversation_messages(conversation_id)
