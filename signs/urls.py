from django.urls import path

from . import views

app_name = "signs"

urlpatterns = [
    path("", views.SignListView.as_view(), name="sign_list"),
    path("<int:pk>/edit/", views.SignUpdateView.as_view(), name="sign_update"),
]