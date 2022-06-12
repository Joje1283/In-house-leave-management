from django.test import TestCase
from django.utils import timezone

from leaves.models import Leave
from members.models import Member
from grants.models import Grant
from orders.models import Order
from ..models import Sign


class TestSign(TestCase):
    def setUp(self) -> None:
        # 휴가 생성
        self.연차 = Leave.objects.create(name="연차", consume=1)
        self.반차 = Leave.objects.create(name="반차", consume=0.5)
        Leave.objects.create(name="무급휴가", consume=0)

        # 유저 생성
        Member.objects.join(username="daniel", password="test")
        Member.objects.join(username="paul", password="test", approver_name="daniel")
        Member.objects.join(username="john", password="test", approver_name="daniel")

        # 휴가 부여
        Grant.objects.grant(username="paul", count=15)
        Grant.objects.grant(username="john", count=15)

        # 휴가 신청
        start_date, end_date = timezone.now().date(), timezone.now().date()
        order_id = Order.objects.order(
            drafter_name="paul",
            is_all_day=True,
            leave_id=self.연차.pk,
            start_date=start_date,
            end_date=end_date,
        )
        order = Order.objects.get(pk=order_id)
        self.sign_id = order.ordersign.sign.pk

    def test_confirm(self):
        approver=Member.objects.get(username="daniel")
        sign = Sign.objects.get(pk=self.sign_id)
        self.assertEqual(sign.sign_type, Sign.SignType.STANDBY)
        sign.confirm(approver)
        sign = Sign.objects.get(pk=self.sign_id)
        self.assertEqual(sign.sign_type, Sign.SignType.CONFIRM)

    def test_reject(self):
        approver = Member.objects.get(username="daniel")
        sign = Sign.objects.get(pk=self.sign_id)
        self.assertEqual(sign.sign_type, Sign.SignType.STANDBY)
        sign.reject(approver)
        sign = Sign.objects.get(pk=self.sign_id)
        self.assertEqual(sign.sign_type, Sign.SignType.REJECT)
