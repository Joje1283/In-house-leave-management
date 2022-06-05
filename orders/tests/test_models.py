from datetime import date

from members.models import Member
from leaves.models import Leave
from grants.models import Grant
from ..exceptions import OutOfLeaveStock
from ..models import Order

from django.test import TestCase


class TestOrder(TestCase):
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

    def test_order(self):
        order_id = Order.objects.order(
            drafter_name="paul",
            is_all_day=True,
            leave_id=self.연차.pk,
            start_date=date(2021, 3, 1),
            end_date=date(2021, 3, 5),
        )
        order = Order.objects.get(pk=order_id)
        self.assertEqual(order.consume, 4)
        self.assertEqual(order.drafter.username, "paul")
        self.assertEqual(order.ordersign.leave, self.연차)

    def test_validate_out_of_leave_stock(self):
        try:
            Order.objects.order(
                drafter_name="paul",
                is_all_day=True,
                leave_id=self.연차.pk,
                start_date=date(2021, 3, 1),
                end_date=date(2021, 3, 30),
            )
        except OutOfLeaveStock:
            return
        self.fail()

