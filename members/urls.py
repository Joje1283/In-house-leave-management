from django.urls import path

from .views import MemberCreateView


app_name = "members"

urlpatterns = [
    path("new/", MemberCreateView.as_view(), name="member_create"),
]
