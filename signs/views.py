from .models import Sign

from django.views.generic import CreateView, UpdateView, ListView


class SignListView(ListView):
    queryset = Sign.objects.order_by("-pk")


class SignUpdateView(UpdateView):
    model = Sign
    success_url = "/signs"
    fields = ["sign_type"]
