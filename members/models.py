from django.contrib.auth.models import AbstractUser
from django.db import models


class Member(AbstractUser):
    approver = models.ForeignKey("self", on_delete=models.DO_NOTHING, null=True, blank=True)
