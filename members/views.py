from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, UpdateView

from .models import Member
from .forms import MemberForm, MemberUpdateForm


class MemberCreateView(CreateView):
    model = Member
    form_class = MemberForm

    def form_valid(self, form):
        self.model.objects.join(**form.cleaned_data)
        return HttpResponseRedirect("/")


class MemberListView(ListView):
    queryset = Member.objects.order_by("-pk")


class MemberUpdateView(UpdateView):
    model = Member
    form_class = MemberUpdateForm
    slug_field = "username"
    template_name = "members/member_update_form.html"

    def form_valid(self, form):
        username = self.kwargs.get("slug")
        approver_name = form.cleaned_data.get("approver").username
        self.model.objects.update_approver(username, approver_name)
        return HttpResponseRedirect("/members")
