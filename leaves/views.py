from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView

from .models import Leave


class LeaveCreateView(LoginRequiredMixin, CreateView):
    model = Leave
    success_url = "/"
    fields = "__all__"


class LeaveListView(LoginRequiredMixin, ListView):
    queryset = Leave.objects.order_by("-pk")


class LeaveUpdateView(LoginRequiredMixin, UpdateView):
    model = Leave
    template_name = "leaves/leave_update_form.html"
    fields = ["consume"]
    success_url = "/leaves"
