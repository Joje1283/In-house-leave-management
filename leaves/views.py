from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView

from .models import Leave


class LeaveCreateView(PermissionRequiredMixin, CreateView):
    model = Leave
    success_url = "/"
    fields = "__all__"
    permission_required = "leaves.add_leave"
    permission_denied_message = "people팀 계정으로 로그인 바랍니다."

    def handle_no_permission(self):
        auth_logout(self.request)
        messages.info(self.request, self.permission_denied_message, "danger")
        return super(LeaveCreateView, self).handle_no_permission()


class LeaveListView(PermissionRequiredMixin, ListView):
    queryset = Leave.objects.order_by("-pk")
    permission_required = "leaves.view_leave"
    permission_denied_message = "people팀 계정으로 로그인 바랍니다."

    def handle_no_permission(self):
        auth_logout(self.request)
        messages.info(self.request, self.permission_denied_message, "danger")
        return super(LeaveListView, self).handle_no_permission()


class LeaveUpdateView(PermissionRequiredMixin, UpdateView):
    model = Leave
    template_name = "leaves/leave_update_form.html"
    fields = ["consume"]
    success_url = "/leaves"
    permission_required = "leaves.change_leave"
    permission_denied_message = "people팀 계정으로 로그인 바랍니다."

    def handle_no_permission(self):
        auth_logout(self.request)
        messages.info(self.request, self.permission_denied_message, "danger")
        return super(LeaveUpdateView, self).handle_no_permission()
