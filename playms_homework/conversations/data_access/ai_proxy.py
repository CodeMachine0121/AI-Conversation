from typing import Dict, Any


class AIProxy:
    """
    Proxy for AI service that always returns "Hello, World!".
    This class provides an abstraction layer for interacting with AI services.
    In a real-world scenario, this would make API calls to an AI service.
    """

    @staticmethod
    def generate_response(user_message: str, context: Dict[str, Any] = None) -> str:
        """
        Generate a response to a user message.

        Args:
            user_message: The message from the user.
            context: Optional context information for the AI.

        Returns:
            Always returns "Hello, World!" as specified in the requirements.
        """
        # In a real implementation, this would call an external AI API
        # and pass the user_message and context
        return "Hello, World!"
