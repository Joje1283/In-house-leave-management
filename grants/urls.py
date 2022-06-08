from django.urls import path
from . import views

app_name = "grants"

urlpatterns = [
    path("new/", views.GrantCreateView.as_view(), name="grant_create"),
    path("", views.GrantListView.as_view(), name="grant_list"),
    path("<int:pk>/delete/", views.GrantDeleteView.as_view(), name="grant_delete"),
]