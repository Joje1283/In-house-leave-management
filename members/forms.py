from .models import Member
from django.contrib.auth.forms import UserCreationForm
from django import forms


class MemberForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Member
        fields = ("username", "approver",)

    def clean(self):
        cleaned_data = self.cleaned_data
        return {
            "username": cleaned_data.get("username"),
            "approver_name": cleaned_data.get("approver").username,
            "password": cleaned_data.get("password2")
        }


class MemberUpdateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ("approver",)
