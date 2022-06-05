from django.contrib import admin
from .models import Grant, OrderSign


@admin.register(Grant)
class GrantAdmin(admin.ModelAdmin):
    list_display = ["member", "stock"]


@admin.register(OrderSign)
class OrderSignAdmin(admin.ModelAdmin):
    list_display = ["leave"]
