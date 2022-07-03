from __future__ import annotations

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.mail import send_mail
from django.db import models
from django.db.models import Sum
from django.template.loader import render_to_string
from django.conf import settings

from members.exceptions import NotFoundMember, DuplicateMember
from grants.models import Grant
from orders.models import Order
from signs.models import Sign


class MemberManager(UserManager):
    def join(self, username: str, password: str, approver_name: str = None):
        self.validate_duplicate_member(username)
        approver = None
        if approver_name:
            approver = self.get_or_validate_not_found_member(username=approver_name)
        new_member = self.model(username=username, approver=approver)
        new_member.set_password(password)
        new_member.save()

    def update_approver(self, username: str, approver_name: str):
        approver = self.get_or_validate_not_found_member(username=approver_name)
        target_member = self.get_or_validate_not_found_member(username=username)
        target_member.approver = approver
        target_member.save()

    def get_or_validate_not_found_member(self, username: str):
        member = self.filter(username=username).first()
        if not member:
            raise NotFoundMember(f"멤버를 찾을 수 없습니다. {username}")
        return member

    def validate_duplicate_member(self, username: str):
        if self.filter(username=username).exists():
            raise DuplicateMember("이미 존재하는 회원입니다.")


class Member(AbstractUser):
    approver = models.ForeignKey(verbose_name="결재자", to="self", on_delete=models.DO_NOTHING, null=True, blank=True)

    objects = MemberManager()

    @property
    def granted_leave_count(self):
        return Grant.objects.granted_stock(username=self.username)

    @property
    def consumed_leave_count(self):
        order_id_list = Sign.objects.filter(sign_type=Sign.SignType.CONFIRM).values_list("ordersign__order", flat=True)
        order_qs = Order.objects.filter(drafter=self)
        order_qs = order_qs.filter(id__in=order_id_list)
        consume_sum = order_qs.aggregate(Sum("consume"))
        result = consume_sum.get("consume__sum")
        if result is None:
            result = 0
        return result

    @property
    def remaining_leave_count(self):
        return self.granted_leave_count - self.consumed_leave_count

    def is_group(self, name):
        return self.groups.filter(name=name).exists()

    def send_welcome_email(self):
        subject = render_to_string('members/welcome_email_subject.txt')
        content = render_to_string('members/welcome_email_content.txt', {
            "user": self,
        })
        sender_email = settings.WELCOME_EMAIL_SENDER
        return send_mail(subject, content, sender_email, [self.email], fail_silently=False)
