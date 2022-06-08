from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
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


class MemberCreateView(LoginRequiredMixin, CreateView):
    model = Member
    form_class = MemberForm

    def form_valid(self, form):
        try:
            self.model.objects.join(**form.cleaned_data)
        except DuplicateMember as e:
            form.add_error("username", e)
            return self.form_invalid(form)
        return HttpResponseRedirect("/")


class MemberListView(LoginRequiredMixin, ListView):
    queryset = Member.objects.order_by("-pk")


class MemberUpdateView(LoginRequiredMixin, UpdateView):
    model = Member
    form_class = MemberUpdateForm
    slug_field = "username"
    template_name = "members/member_update_form.html"

    def form_valid(self, form):
        username = self.kwargs.get("slug")
        approver_name = form.cleaned_data.get("approver").username
        self.model.objects.update_approver(username, approver_name)
        return HttpResponseRedirect("/members")
