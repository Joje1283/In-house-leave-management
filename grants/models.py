from django.db import models


class Grant(models.Model):
    member = models.ForeignKey(verbose_name="휴가 대상자", to="members.Member", on_delete=models.CASCADE)
    stock = models.FloatField(verbose_name="부여된 휴가 일 수")

    def __str__(self):
        return f"{self.member}에게 {self.stock}일 부여"


class GrantLeave(models.Model):
    grant = models.ForeignKey(to="grants.Grant", on_delete=models.DO_NOTHING)
    leave = models.ForeignKey(to="leaves.Leave", on_delete=models.DO_NOTHING)
    sign = models.OneToOneField(verbose_name="승인 정보", to="signs.Sign", on_delete=models.DO_NOTHING, null=True)
    order = models.OneToOneField(verbose_name="신청 정보", to="orders.Order", on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"{self.grant} - {self.leave}"
