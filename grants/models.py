from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model

from grants.exceptions import RemoveGrantException


class GrantManager(models.Manager):
    def grant(self, username, count):
        member = get_user_model().objects.get_or_validate_not_found_member(username)
        grant = self.model(member=member, stock=count)
        grant.save()
        return grant

    def granted_stock(self, username):
        data = self.filter(member__username=username).aggregate(Sum("stock"))
        result = data.get("stock__sum")
        if result is None:
            result = 0
        return result

    def remove_grant(self, pk):
        target_grant = self.filter(pk=pk).first()
        if target_grant:
            remaining_leave_count, delete_leave_count = target_grant.member.remaining_leave_count, target_grant.stock
            if remaining_leave_count < delete_leave_count:
                raise RemoveGrantException(f"남은 휴가가 부족합니다.\n삭제할 휴가: {delete_leave_count}, 남은 휴가: {remaining_leave_count}")
            target_grant.delete()


class Grant(models.Model):
    member = models.ForeignKey(verbose_name="휴가 대상자", to="members.Member", on_delete=models.CASCADE)
    stock = models.FloatField(verbose_name="부여된 휴가 일 수")

    objects = GrantManager()

    def __str__(self):
        return f"{self.member}에게 {self.stock}일 부여"


class OrderSign(models.Model):
    leave = models.ForeignKey(to="leaves.Leave", on_delete=models.DO_NOTHING)
    sign = models.OneToOneField(verbose_name="승인 정보", to="signs.Sign", on_delete=models.DO_NOTHING, null=True)
    order = models.OneToOneField(verbose_name="신청 정보", to="orders.Order", on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"{self.sign} - {self.order}"
