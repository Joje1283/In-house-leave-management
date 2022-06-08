from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView

from .exceptions import OutOfLeaveStock
from .forms import OrderForm
from .models import Order


class OrderListView(LoginRequiredMixin, ListView):
    model = Order

    def get_queryset(self):
        qs: QuerySet[Order] = super(OrderListView, self).get_queryset()
        qs = qs.filter(drafter=self.request.user)
        return qs


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm

    def form_valid(self, form):
        try:
            self.model.objects.order(**form.cleaned_data)
        except OutOfLeaveStock as e:
            form.add_error(None, e)
            return super(OrderCreateView, self).form_invalid(form)
        return HttpResponseRedirect("/orders")

    def get_form_kwargs(self):
        """폼에 keyword arguments를 주입한다"""
        # grab the current set of form #kwargs
        kwargs = super().get_form_kwargs()
        # Update the kwargs with the user_id
        kwargs['user'] = self.request.user
        return kwargs
