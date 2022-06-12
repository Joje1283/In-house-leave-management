from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView

from .exceptions import DuplicateMember
from .models import Member
from .forms import MemberForm, MemberUpdateForm

from django.contrib.auth.views import (
    LoginView, logout_then_login,
)


class CustomLoginView(LoginView):
    template_name = "members/login_form.html"

    def form_valid(self, form):
        messages.success(self.request, '로그인 성공!')
        return super(CustomLoginView, self).form_valid(form)


def logout(request):
    messages.success(request, '로그아웃 되었습니다.')
    return logout_then_login(request)


class MemberCreateView(PermissionRequiredMixin, CreateView):
    model = Member
    form_class = MemberForm
    permission_required = ("members.add_member",)
    permission_denied_message = "people팀 계정으로 로그인 바랍니다."

    def form_valid(self, form):
        try:
            self.model.objects.join(**form.cleaned_data)
        except DuplicateMember as e:
            form.add_error("username", e)
            return self.form_invalid(form)
        return HttpResponseRedirect("/")

    def handle_no_permission(self):
        auth_logout(self.request)
        messages.info(self.request, self.permission_denied_message, "danger")
        return super(MemberCreateView, self).handle_no_permission()


class MemberListView(PermissionRequiredMixin, ListView):
    queryset = Member.objects.order_by("-pk")
    permission_required = "members.view_member"
    permission_denied_message = "people팀 계정으로 로그인 바랍니다."

    def handle_no_permission(self):
        auth_logout(self.request)
        messages.info(self.request, self.permission_denied_message, "danger")
        return super(MemberListView, self).handle_no_permission()


class MemberUpdateView(PermissionRequiredMixin, UpdateView):
    model = Member
    form_class = MemberUpdateForm
    slug_field = "username"
    template_name = "members/member_update_form.html"
    permission_required = "members.change_member"
    permission_denied_message = "people팀 계정으로 로그인 바랍니다."

    def form_valid(self, form):
        username = self.kwargs.get("slug")
        approver_name = form.cleaned_data.get("approver").username
        self.model.objects.update_approver(username, approver_name)
        return HttpResponseRedirect("/members")

    def handle_no_permission(self):
        auth_logout(self.request)
        messages.info(self.request, self.permission_denied_message, "danger")
        return super(MemberUpdateView, self).handle_no_permission()
