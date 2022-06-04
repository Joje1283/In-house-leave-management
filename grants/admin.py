from django.contrib import admin
from .models import Grant, GrantLeave


@admin.register(Grant)
class GrantAdmin(admin.ModelAdmin):
    list_display = ["member", "stock"]


@admin.register(GrantLeave)
class GrantLeave(admin.ModelAdmin):
    list_display = ["grant", "leave"]