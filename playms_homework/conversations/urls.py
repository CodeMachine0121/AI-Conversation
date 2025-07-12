from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .presentation.conversation_management_views import ConversationManagementViewSet
from .presentation.conversation_views import ConversationViewSet
from .presentation.chat_setting_views import ChatSettingViewSet
from .presentation.user_views import UserManagementViewSet
from .views import ChatView, ChatSettingView, ChatConversationManagerView

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'chat-setting', ChatSettingViewSet, basename='chat-setting')

# 管理員專用路由
management_router = DefaultRouter()
management_router.register(r'conversations', ConversationManagementViewSet, basename='admin-conversation')
management_router.register(r'users', UserManagementViewSet, basename='admin-users')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path("chat/", ChatView.as_view(), name="chat"),
    path("setting/", ChatSettingView.as_view(), name="chat-setting"),
    path('manage/', ChatConversationManagerView.as_view(), name='conversation-management'),

    path('api/', include(router.urls)),
    path('api/admin/', include(management_router.urls)),
]
