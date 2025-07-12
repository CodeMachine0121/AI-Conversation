from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()

class UserManagementViewSet(ViewSet):
    """
    Admin-only viewset for getting user list
    """
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]

    def list(self, request):
        """
        List all users for admin filtering
        """
        users = User.objects.filter(is_active=True).values('id', 'username').order_by('username')
        return Response(list(users))
