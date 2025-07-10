from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class ChatView(LoginRequiredMixin, TemplateView):
    template_name = "conversations/chat.html"