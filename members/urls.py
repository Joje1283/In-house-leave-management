from django.urls import path

from .views import MemberCreateView, MemberListView, MemberUpdateView


app_name = "members"

urlpatterns = [
    path("new/", MemberCreateView.as_view(), name="member_create"),
    path("", MemberListView.as_view(), name="member_list"),
    path("<slug:slug>/edit", MemberUpdateView.as_view(), name="member_update"),
]
