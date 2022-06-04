from django.db import models


class Leave(models.Model):
    name = models.CharField(verbose_name="휴가 종류", max_length=30)
    consume = models.IntegerField(verbose_name="소진일")
