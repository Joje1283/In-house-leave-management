from .models import PushMessage

from django.contrib import admin


@admin.register(PushMessage)
class PushMessageAdmin(admin.ModelAdmin):
    list_display = ["push_key", "title", "message"]
