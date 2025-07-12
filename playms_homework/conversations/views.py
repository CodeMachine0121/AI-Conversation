from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

class ChatView(LoginRequiredMixin, TemplateView):
    template_name = "conversations/chat.html"

@method_decorator(staff_member_required, name='dispatch')
class ChatConversationManagerView(LoginRequiredMixin, TemplateView):
    template_name = "conversations/chat_conversation_manager.html"

class ChatSettingView(LoginRequiredMixin, TemplateView):
    pass
