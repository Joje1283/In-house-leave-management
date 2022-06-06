from django.http import HttpResponseRedirect
from django.views.generic import CreateView

from .models import Member
from .forms import MemberForm


class MemberCreateView(CreateView):
    model = Member
    form_class = MemberForm

    def form_valid(self, form):
        self.model.objects.join(**form.cleaned_data)
        return HttpResponseRedirect("/")
