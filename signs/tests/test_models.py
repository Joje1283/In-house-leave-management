from django.test import TestCase
from django.utils import timezone

from leaves.models import Leave
from members.models import Member
from grants.models import Grant
from orders.models import Order
from push.models import PushMessage
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

        # 푸시 메시지 생성
        PushMessage.objects.create(push_key="APPROVE", title="휴가가 수락되었습니다.", message="{name}이(가) 휴가를 수락합니다.")  # 휴가 수락
        PushMessage.objects.create(push_key="DENY", title="휴가가 반려되었습니다.",
                                   message="{name}이(가) 휴가를 반려합니다. \n사유: {reason}")  # 휴가 반려
        PushMessage.objects.create(push_key="REQUEST", title="휴가 요청", message="{name}이(가) 휴가를 요청합니다.")  # 휴가 신청
        PushMessage.objects.create(push_key="CANCEL", title="휴가 취소", message="{name}이(가) 휴가를 취소합니다.")  # 휴가 취소

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
