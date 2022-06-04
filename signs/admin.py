from django.contrib import admin
from .models import Sign


@admin.register(Sign)
class SignAdmin(admin.ModelAdmin):
    list_display = ["approver", "sign_type"]
