from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, DeleteView

from .exceptions import RemoveGrantException
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

    def form_valid(self, form):
        try:
            pk = self.kwargs.get("pk")
            Grant.objects.remove_grant(pk)
        except RemoveGrantException as e:
            form.add_error(None, e)
            return self.form_invalid(form)
        return HttpResponseRedirect("/grants")
