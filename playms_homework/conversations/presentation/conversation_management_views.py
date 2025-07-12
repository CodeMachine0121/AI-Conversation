from rest_framework.viewsets import ViewSet

class ConversationManagementViewSet(ViewSet):
    def __init__(self, conversation_service):
        self.conversation_service = conversation_service
