from typing import List, Optional

from ..models import Conversation, Message


class ConversationRepository:
    """
    Repository for accessing Conversation and Message models.
    This class provides an abstraction layer between the business logic and the database.
    """

    @staticmethod
    def get_conversation(conversation_id: int) -> Optional[Conversation]:
        """
        Get a conversation by ID.

        Args:
            conversation_id: The ID of the conversation to retrieve.

        Returns:
            The conversation if found, None otherwise.
        """
        try:
            return Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return None

    @staticmethod
    def get_user_conversations(user_id: int) -> List[Conversation]:
        """
        Get all conversations for a user.

        Args:
            user_id: The ID of the user.

        Returns:
            A list of conversations for the user.
        """
        return list(Conversation.objects.filter(user_id=user_id))

    @staticmethod
    def create_conversation(user_id: int) -> Conversation:
        """
        Create a new conversation for a user.

        Args:
            user_id: The ID of the user.

        Returns:
            The newly created conversation.
        """
        return Conversation.objects.create(user_id=user_id)

    @staticmethod
    def update_conversation_status(conversation_id: int, status: str) -> Optional[Conversation]:
        """
        Update the status of a conversation.

        Args:
            conversation_id: The ID of the conversation to update.
            status: The new status.

        Returns:
            The updated conversation if found, None otherwise.
        """
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            conversation.status = status
            conversation.save()
            return conversation
        except Conversation.DoesNotExist:
            return None

    @staticmethod
    def add_message(conversation_id: int, sender: str, content: str) -> Optional[Message]:
        """
        Add a message to a conversation.

        Args:
            conversation_id: The ID of the conversation.
            sender: The sender of the message (user or ai).
            content: The content of the message.

        Returns:
            The newly created message if the conversation exists, None otherwise.
        """
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            message = Message.objects.create(
                conversation=conversation,
                sender=sender,
                content=content
            )
            # Update the conversation's updated_at timestamp
            conversation.save()
            return message
        except Conversation.DoesNotExist:
            return None

    @staticmethod
    def get_conversation_messages(conversation_id: int) -> List[Message]:
        """
        Get all messages for a conversation.

        Args:
            conversation_id: The ID of the conversation.

        Returns:
            A list of messages for the conversation.
        """
        return list(Message.objects.filter(conversation_id=conversation_id))
