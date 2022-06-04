from django.db import models
from django.conf import settings


class Order(models.Model):
    drafter = models.ForeignKey(verbose_name="신청자", to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    start_date = models.DateField(verbose_name="휴가 시작일")
    end_date = models.DateField(verbose_name="휴가 종료일")

    def __str__(self):
        return f"{self.drafter} ({self.start_date} ~ {self.end_date})"