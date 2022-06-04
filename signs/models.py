from django.db import models
from django.conf import settings


class Sign(models.Model):
    approver = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    order = models.OneToOneField(to="grants.GrantLeave", on_delete=models.DO_NOTHING)

    class SignType(models.TextChoices):
        CONFIRM = "CONFIRM"
        REJECT = "REJECT"
        STANDBY = "STANDBY"

    sign_type = models.CharField(max_length=20, choices=SignType.choices, default=SignType.STANDBY)
