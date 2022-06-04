from django.db import models
from django.conf import settings


class Order(models.Model):
    grant_leave_id = models.OneToOneField(to="grants.GrantLeave", on_delete=models.DO_NOTHING)
    drafter = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    start_date = models.DateField(verbose_name="휴가 시작일")
    end_date = models.DateField(verbose_name="휴가 종료일")
