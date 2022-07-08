from django.db import models
from django.conf import settings

from push.models import PushMessage
from .exceptions import OutOfLeaveStock, NotApproverError


class Sign(models.Model):
    approver = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)

    class SignType(models.TextChoices):
        CONFIRM = "CONFIRM", "수락됨"
        REJECT = "REJECT", "거절됨"
        STANDBY = "STANDBY", "대기"

    sign_type = models.CharField(max_length=20, choices=SignType.choices, default=SignType.STANDBY)

    def __str__(self):
        return f"{self.approver} - {self.sign_type}"

    def confirm(self, approver):
        if self.approver != approver:
            raise NotApproverError("결재자만 결재가 가능합니다.")
        self.sign_type = self.SignType.CONFIRM
        drafter = self.ordersign.order.drafter
        approve_leave_count = self.ordersign.order.consume
        if drafter.remaining_leave_count < approve_leave_count:
            raise OutOfLeaveStock("휴가가 부족합니다.")
        self.save()
        from push.tasks import send_email_push
        title, message = PushMessage.get_message(
            push_key=PushMessage.PushType.APPROVE_BY_APPROVER,
            name=approver.username
        )
        send_email_push.apply_async([  # params: from_address, to_address_list, subject, content
            settings.WELCOME_EMAIL_SENDER,
            self.ordersign.order.drafter.email,
            title,
            message
        ], queue="paul_worker")

    def reject(self, approver):
        if self.approver != approver:
            raise NotApproverError("결재자만 결재가 가능합니다.")
        self.sign_type = self.SignType.REJECT
        self.save()
        from push.tasks import send_email_push
        title, message = PushMessage.get_message(
            push_key=PushMessage.PushType.DENY_BY_APPROVER,
            name=approver.username
        )
        send_email_push.apply_async([  # params: from_address, to_address_list, subject, content
            settings.WELCOME_EMAIL_SENDER,
            self.ordersign.order.drafter.email,
            title,
            message
        ], queue="paul_worker")

    def cancel(self, approver):
        if self.approver != approver:
            raise NotApproverError("결재자만 수정이 가능합니다.")
        self.sign_type = self.SignType.STANDBY
        self.save()

    @property
    def sign_type_to_message(self):
        return [choice[1] for choice in self.SignType.choices if choice[0] == self.sign_type][0]
