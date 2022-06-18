from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from .exceptions import OutOfLeaveStock, NotApproverError
from .models import Sign

from django.views.generic import UpdateView, ListView


class SignListView(LoginRequiredMixin, ListView):
    queryset = Sign.objects.order_by("-pk")

    def get_queryset(self):
        qs = super(SignListView, self).get_queryset()
        qs = qs.select_related("ordersign__order", "ordersign__order__drafter")
        qs = qs.filter(approver=self.request.user)
        return qs


class SignUpdateView(LoginRequiredMixin, UpdateView):
    model = Sign
    success_url = "/signs"
    fields = ["sign_type"]

    def form_valid(self, form):
        try:
            pk = self.kwargs.get("pk")
            sign = Sign.objects.get(pk=pk)
            sign_type = form.cleaned_data.get("sign_type")
            approver = self.request.user
            if sign_type == Sign.SignType.CONFIRM:
                sign.confirm(approver)
            elif sign_type == Sign.SignType.REJECT:
                sign.reject(approver)
            else:
                sign.cancel(approver)
            return HttpResponseRedirect("/signs")
        except OutOfLeaveStock as e:
            form.add_error(None, e)
            return self.form_invalid(form)
        except NotApproverError as e:
            form.add_error(None, e)
            return self.form_invalid(form)
