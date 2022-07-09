import sys
from datetime import date

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

from grants.models import OrderSign, Grant
from leaves.models import Leave
from orders.exceptions import OutOfLeaveStock, StartedLeaveCancelImpossible
from push.models import PushMessage
from signs.models import Sign


class OrderManager(models.Manager):
    def order(
            self,
            drafter_name: str,
            is_all_day: bool,
            leave_id: int,
            start_date: date = None,
            end_date: date = None
    ):
        # 엔티티 조회
        member_model = get_user_model()
        drafter = member_model.objects.get_or_validate_not_found_member(drafter_name)
        approver = drafter.approver
        leave = Leave.objects.get(pk=leave_id)

        # 휴가 소진일 계산
        consume: int = leave.consume
        if is_all_day:
            consume = (end_date - start_date).days + 1

        # 잔여 휴가 확인
        self.validate_out_of_leave_stock(drafter=drafter, consume=consume)

        # 신청 생성
        order = self.create(
            drafter=drafter,
            start_date=start_date,
            end_date=end_date,
            is_all_day=is_all_day,
            consume=consume
        )

        # 결재 생성
        sign = Sign.objects.create(approver=approver)

        # 신청-결재 매핑
        OrderSign.objects.create(order=order, sign=sign, leave=leave)

        # 푸시 알림
        from push.tasks import send_email_push
        title, message = PushMessage.get_message(push_key=PushMessage.PushType.REQUEST_BY_DRAFTER, name=drafter_name)
        send_email_push.apply_async([  # params: from_address, to_address_list, subject, content
            settings.WELCOME_EMAIL_SENDER,
            approver.email,
            title,
            message
        ], queue="paul_worker")
        return order.pk

    def cancel(self, order_id):
        order = self.get(pk=order_id)
        if order.start_date < timezone.now().date():
            raise StartedLeaveCancelImpossible("지난 휴가는 취소할 수 없습니다.")
        order.canceled = True
        order.save()
        from push.tasks import send_email_push
        title, message = PushMessage.get_message(
            push_key=PushMessage.PushType.CANCEL_BY_DRAFTER,
            name=order.drafter.username
        )
        send_email_push.apply_async([  # params: from_address, to_address_list, subject, content
            settings.WELCOME_EMAIL_SENDER,
            order.ordersign.sign.approver.email,
            title,
            message
        ], queue="paul_worker")

    @staticmethod
    def validate_out_of_leave_stock(drafter, consume):
        remaining_leave_count = drafter.remaining_leave_count
        if remaining_leave_count < consume:
            raise OutOfLeaveStock("휴가가 부족합니다.")


class Order(models.Model):
    drafter = models.ForeignKey(verbose_name="신청자", to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    start_date = models.DateField(verbose_name="휴가 시작일", null=True)
    end_date = models.DateField(verbose_name="휴가 종료일", null=True)
    is_all_day = models.BooleanField(verbose_name="연차 여부",
                                     default=True)  # 연차 Or 연차 아닌지 여부 저장. 연차일 경우 소진일이 start_date, end_date와 함께 계산 필요
    consume = models.FloatField(default=1)
    canceled = models.BooleanField(default=False)

    objects = OrderManager()

    def __str__(self):
        return f"{self.drafter} ({self.start_date} ~ {self.end_date})"
