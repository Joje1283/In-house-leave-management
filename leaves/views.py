from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from .models import Leave


class LeaveCreateView(CreateView):
    model = Leave
    success_url = "/"
    fields = "__all__"


class LeaveListView(ListView):
    queryset = Leave.objects.order_by("-pk")


class LeaveUpdateView(UpdateView):
    model = Leave
    template_name = "leaves/leave_update_form.html"
    fields = ["consume"]
    success_url = "/leaves"
