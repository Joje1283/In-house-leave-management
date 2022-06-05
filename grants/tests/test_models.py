from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Grant


class TestGrant(TestCase):
    def setUp(self) -> None:
        get_user_model().objects.join("daniel", "test")
        get_user_model().objects.join("john", "test", "daniel")
        get_user_model().objects.join("paul", "test", "daniel")

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
