from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class ChatView(LoginRequiredMixin, TemplateView):
    template_name = "conversations/chat.html"

class ChatSettingView(LoginRequiredMixin, TemplateView):
    pass
