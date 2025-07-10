from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .presentation.conversation_views import ConversationViewSet
from .presentation.setting_views import SettingViewSet
from .views import ChatView, ChatSettingView

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path("chat/", ChatView.as_view(), name="chat"),
    path("setting/", ChatSettingView.as_view(), name="chat-setting"),
    path('api/', include(router.urls)),
]
