from datetime import date

from django.test import TestCase

from django.contrib.auth import get_user_model

from leaves.models import Leave
from members.models import Member
from orders.models import Order
from push.models import PushMessage
from ..exceptions import RemoveGrantException
from ..models import Grant


class TestGrant(TestCase):
    def setUp(self) -> None:
        get_user_model().objects.join("daniel", "test")
        get_user_model().objects.join("john", "test", "daniel")
        get_user_model().objects.join("paul", "test", "daniel")
        PushMessage.objects.create(push_key="APPROVE", title="휴가가 수락되었습니다.", message="{name}이(가) 휴가를 수락합니다.")  # 휴가 수락
        PushMessage.objects.create(push_key="DENY", title="휴가가 반려되었습니다.",
                                   message="{name}이(가) 휴가를 반려합니다. \n사유: {reason}")  # 휴가 반려
        PushMessage.objects.create(push_key="REQUEST", title="휴가 요청", message="{name}이(가) 휴가를 요청합니다.")  # 휴가 신청
        PushMessage.objects.create(push_key="CANCEL", title="휴가 취소", message="{name}이(가) 휴가를 취소합니다.")  # 휴가 취소

    def test_grant_and_granted_stock(self):
        # 휴가 부여 및 남은 휴가 확인
        Grant.objects.grant("paul", 10)
        self.assertEqual(Grant.objects.count(), 1)
        self.assertEqual(Grant.objects.granted_stock("paul"), 10)
        Grant.objects.grant("paul", 15)
        self.assertEqual(Grant.objects.count(), 2)
        self.assertEqual(Grant.objects.granted_stock("paul"), 25)

        # 부여되지 않은 유저 남은 휴가 확인
        self.assertEqual(Grant.objects.granted_stock("john"), 0)

    def test_delete_grant_with_error(self):
        # 조건 --------------------
        # 휴가 생성
        self.연차 = Leave.objects.create(name="연차", consume=1)
        self.반차 = Leave.objects.create(name="반차", consume=0.5)
        Leave.objects.create(name="무급휴가", consume=0)

        # 휴가 부여 (10일, 5일  각각 paul에게 부여)
        grant = Grant.objects.grant("paul", 10)
        Grant.objects.grant("paul", 5)
        user = grant.member

        # 휴가 12일 사용
        order_id = Order.objects.order(
            drafter_name="paul",
            is_all_day=True,
            leave_id=self.연차.pk,
            start_date=date(2021, 3, 1),
            end_date=date(2021, 3, 12),
        )
        order = Order.objects.get(pk=order_id)
        approver = Member.objects.get(username="daniel")
        order.ordersign.sign.confirm(approver)

        # THEN ---------------------
        # 생성했던 10일 휴가 삭제하기
        try:
            Grant.objects.remove_grant(grant.pk)
        except RemoveGrantException:
            return
        self.fail("휴가 삭제에 실패해야 합니다.")

    def test_delete_grant(self):
        # 조건 --------------------
        # 휴가 생성
        self.연차 = Leave.objects.create(name="연차", consume=1)
        self.반차 = Leave.objects.create(name="반차", consume=0.5)
        Leave.objects.create(name="무급휴가", consume=0)

        # 휴가 부여 (10일, 5일  각각 paul에게 부여)
        Grant.objects.grant("paul", 10)
        grant = Grant.objects.grant("paul", 5)
        user = grant.member
        self.assertEqual(grant.member.remaining_leave_count, 15)

        # 휴가 12일 사용
        order_id = Order.objects.order(
            drafter_name="paul",
            is_all_day=True,
            leave_id=self.연차.pk,
            start_date=date(2021, 3, 1),
            end_date=date(2021, 3, 5),
        )

        order = Order.objects.get(pk=order_id)
        sign = order.ordersign.sign
        approver = Member.objects.get(username="daniel")
        sign.confirm(approver)
        self.assertEqual(grant.member.remaining_leave_count, 10)

        # THEN ---------------------
        # 생성했던 5일 휴가 삭제하기
        Grant.objects.remove_grant(grant.pk)
        self.assertEqual(grant.member.remaining_leave_count, 5)
