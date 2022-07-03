from django.urls import path
from . import views

app_name = "push"

urlpatterns = [
    path("debug/", views.debug, name="debug"),
]