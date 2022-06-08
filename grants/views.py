from django.views.generic import ListView, CreateView, DeleteView

from .models import Grant


class GrantListView(ListView):
    queryset = Grant.objects.order_by("-pk")


class GrantCreateView(CreateView):
    model = Grant
    fields = ["member", "stock"]
    success_url = "/grants"


class GrantDeleteView(DeleteView):
    model = Grant
    success_url = "/grants"
