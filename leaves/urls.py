from django.urls import path

from . import views

app_name = "leaves"

urlpatterns = [
    path("new/", views.LeaveCreateView.as_view(), name="leave_create"),
    path("", views.LeaveListView.as_view(), name="leave_list"),
    path("<int:pk>/edit/", views.LeaveUpdateView.as_view(), name="leave_update"),
]