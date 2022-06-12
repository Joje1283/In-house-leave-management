from django import forms
from django.utils import timezone

from .models import Order
from leaves.models import Leave


class OrderForm(forms.ModelForm):
    leave = forms.ModelChoiceField(Leave.objects.all())

    class Meta:
        model = Order
        fields = ["start_date", "end_date", "leave"]
        help_texts = {
            "start_date": "yyyy-mm-dd",
            "end_date": "yyyy-mm-dd, 연차 이외의 휴가는 시작일과 동일하게 저장됩니다."
        }

    def __init__(self, *args, **kwargs):
        # set the user as an attribute of the form
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_start_date(self):
        start_date = self.cleaned_data.get("start_date")
        if start_date < timezone.now().date():
            self.add_error("start_date", "이전 날짜는 신청할 수 없습니다.")
        return start_date

    def clean(self):
        cleaned_data = self.cleaned_data
        leave = cleaned_data.get("leave")
        is_all_day = False
        if leave.name == "연차":
            is_all_day = True
        else:
            cleaned_data["end_date"] = cleaned_data["start_date"]
        if is_all_day and cleaned_data["end_date"] < cleaned_data["start_date"]:
            self.add_error("end_date", "종료일이 시작일보다 빠릅니다.")
        return {
            "drafter_name": self.user.username,
            "start_date": cleaned_data.get("start_date"),
            "end_date": cleaned_data.get("end_date"),
            "leave_id": leave.pk,
            "is_all_day": is_all_day
        }
