from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views.generic import ListView

from .models import Order


class OrderListView(LoginRequiredMixin, ListView):
    model = Order

    def get_queryset(self):
        qs: QuerySet[Order] = super(OrderListView, self).get_queryset()
        qs = qs.filter(drafter=self.request.user)
        return qs
