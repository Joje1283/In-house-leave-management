from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView

from .models import Grant


class GrantListView(LoginRequiredMixin, ListView):
    queryset = Grant.objects.order_by("-pk")


class GrantCreateView(LoginRequiredMixin, CreateView):
    model = Grant
    fields = ["member", "stock"]
    success_url = "/grants"


class GrantDeleteView(LoginRequiredMixin, DeleteView):
    model = Grant
    success_url = "/grants"
