from django.db import models


class Grant(models.Model):
    member = models.ForeignKey(verbose_name="휴가 대상자", to="members.Member", on_delete=models.CASCADE)
    stock = models.IntegerField(verbose_name="부여된 휴가 일 수")
