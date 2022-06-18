from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib import messages

from .exceptions import RemoveGrantException
from .models import Grant


class GrantListView(PermissionRequiredMixin, ListView):
    queryset = Grant.objects.select_related("member").order_by("-pk")
    permission_required = "grants.view_grant"
    permission_denied_message = "people팀 계정으로 로그인 바랍니다."

    def handle_no_permission(self):
        auth_logout(self.request)
        messages.info(self.request, self.permission_denied_message, "danger")
        return super(GrantListView, self).handle_no_permission()


class GrantCreateView(PermissionRequiredMixin, CreateView):
    model = Grant
    fields = ["member", "stock", "description"]
    success_url = "/grants"
    permission_required = "grants.add_grant"
    permission_denied_message = "people팀 계정으로 로그인 바랍니다."

    def handle_no_permission(self):
        auth_logout(self.request)
        messages.info(self.request, self.permission_denied_message, "danger")
        return super(GrantCreateView, self).handle_no_permission()


class GrantDeleteView(PermissionRequiredMixin, DeleteView):
    model = Grant
    success_url = "/grants"
    permission_required = "grants.change_grant"
    permission_denied_message = "people팀 계정으로 로그인 바랍니다."

    def form_valid(self, form):
        try:
            pk = self.kwargs.get("pk")
            Grant.objects.remove_grant(pk)
        except RemoveGrantException as e:
            form.add_error(None, e)
            return self.form_invalid(form)
        return HttpResponseRedirect("/grants")

    def handle_no_permission(self):
        auth_logout(self.request)
        messages.info(self.request, self.permission_denied_message, "danger")
        return super(GrantDeleteView, self).handle_no_permission()
