from django.db import models
from django.conf import settings


class Sign(models.Model):
    approver = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    class SignType(models.TextChoices):
        CONFIRM = "CONFIRM"
        REJECT = "REJECT"
        STANDBY = "STANDBY"

    sign_type = models.CharField(max_length=20, choices=SignType.choices, default=SignType.STANDBY)

    def __str__(self):
        return f"{self.approver} - {self.sign_type}"

    def confirm(self):
        self.sign_type = self.SignType.CONFIRM
        self.save()

    def reject(self):
        self.sign_type = self.SignType.REJECT
        self.save()
