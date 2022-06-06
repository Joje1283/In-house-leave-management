from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import SelectDateWidget

from .models import Order
from leaves.models import Leave

"""
drafter_name
is_all_day
leave_id
start_date
end_date
"""


class OrderForm(forms.ModelForm):
    leave = forms.ModelChoiceField(Leave.objects.all())

    class Meta:
        model = Order
        fields = ["start_date", "end_date", "leave"]
        help_texts = {
            "start_date": "yyyy-mm-dd",
            "end_date": "yyyy-mm-dd"
        }

    def __init__(self, *args, **kwargs):
        # set the user as an attribute of the form
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        leave = cleaned_data.get("leave")
        is_all_day = False
        if leave.name == "연차":
            is_all_day = True
        return {
            "drafter_name": self.user.username,
            "start_date": cleaned_data.get("start_date"),
            "end_date": cleaned_data.get("end_date"),
            "leave_id": leave.pk,
            "is_all_day": is_all_day
        }
