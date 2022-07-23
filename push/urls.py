from django.urls import path
from . import views

app_name = "push"

urlpatterns = [
    path("debug/", views.debug, name="debug"),  # 테스트 안할때는 주석 처리
]