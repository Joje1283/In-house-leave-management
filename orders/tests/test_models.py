from datetime import date

from django.utils import timezone

from members.models import Member
from leaves.models import Leave
from grants.models import Grant, OrderSign
from push.models import PushMessage
from signs.models import Sign
from ..exceptions import OutOfLeaveStock, StartedLeaveCancelImpossible
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

        # 푸시 메시지 생성
        PushMessage.objects.create(push_key="APPROVE", title="휴가가 수락되었습니다.", message="{name}이(가) 휴가를 수락합니다.")  # 휴가 수락
        PushMessage.objects.create(push_key="DENY", title="휴가가 반려되었습니다.",
                                   message="{name}이(가) 휴가를 반려합니다. \n사유: {reason}")  # 휴가 반려
        PushMessage.objects.create(push_key="REQUEST", title="휴가 요청", message="{name}이(가) 휴가를 요청합니다.")  # 휴가 신청
        PushMessage.objects.create(push_key="CANCEL", title="휴가 취소", message="{name}이(가) 휴가를 취소합니다.")  # 휴가 취소

    def test_order(self):
        order_id = Order.objects.order(
            drafter_name="paul",
            is_all_day=True,
            leave_id=self.연차.pk,
            start_date=date(2021, 3, 1),
            end_date=date(2021, 3, 5),
        )
        order = Order.objects.get(pk=order_id)
        self.assertEqual(order.consume, 5)
        self.assertEqual(order.drafter.username, "paul")
        self.assertEqual(order.ordersign.leave, self.연차)

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Sign.objects.count(), 1)
        self.assertEqual(OrderSign.objects.count(), 1)

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

    def test_cancel(self):
        # given
        start_date, end_date = timezone.now().date(), timezone.now().date()
        order_id = Order.objects.order(
            drafter_name="paul",
            is_all_day=True,
            leave_id=self.연차.pk,
            start_date=start_date,
            end_date=end_date,
        )
        self.assertIsNotNone(Order.objects.get(pk=order_id))
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Sign.objects.count(), 1)
        self.assertEqual(OrderSign.objects.count(), 1)
        order = Order.objects.get(pk=order_id)
        self.assertFalse(order.canceled)

        # when
        Order.objects.cancel(order_id)

        # then
        # order, sign, ordersign의 레코드가 삭제되었는지 확인
        order = Order.objects.get(pk=order_id)
        self.assertTrue(order.canceled)

    def test_이미_시작한_휴가_취소하기(self):
        # when
        start_date, end_date = date(2022, 5, 1), date(2022, 5, 1)
        order_id = Order.objects.order(
            drafter_name="paul",
            is_all_day=True,
            leave_id=self.연차.pk,
            start_date=start_date,
            end_date=end_date,
        )
        try:
            Order.objects.cancel(order_id=order_id)
        except StartedLeaveCancelImpossible:
            return
        self.fail("취소되면 안됩니다.")


