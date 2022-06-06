from django.urls import path

from .views import MemberCreateView, MemberListView, MemberUpdateView, logout, CustomLoginView


app_name = "members"

urlpatterns = [
    path("new/", MemberCreateView.as_view(), name="member_create"),
    path("", MemberListView.as_view(), name="member_list"),
    path("<slug:slug>/edit", MemberUpdateView.as_view(), name="member_update"),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
]
