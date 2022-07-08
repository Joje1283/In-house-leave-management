
from django.conf import settings
from django.test import TestCase
from django.test.runner import DiscoverRunner
from .models import PushMessage
from celery import current_app


class TestRunner(DiscoverRunner):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def __disable_celery():
        settings.CELERY_BROKER_URL = current_app.conf.CELERY_BROKER_URL = f'filesystem:///dev/null/'
        settings.BROKER_TRANSPORT_OPTIONS = current_app.conf.BROKER_TRANSPORT_OPTIONS = {
            'data_folder_in': '/tmp',
            'data_folder_out': '/tmp',
            'data_folder_processed': '/tmp',
        }

    def setup_test_environment(self, **kwargs):
        TestRunner.__disable_celery()
        super(TestRunner, self).setup_test_environment(**kwargs)


class TestPushMessage(TestCase):
    def setUp(self) -> None:
        PushMessage.objects.create(push_key="APPROVE", title="휴가가 수락되었습니다.", message="{name}이(가) 휴가를 수락합니다.")  # 휴가 수락
        PushMessage.objects.create(push_key="DENY", title="휴가가 반려되었습니다.", message="{name}이(가) 휴가를 반려합니다. \n사유: {reason}")  # 휴가 반려
        PushMessage.objects.create(push_key="REQUEST", title="휴가 요청", message="{name}이(가) 휴가를 요청합니다.")  # 휴가 신청
        PushMessage.objects.create(push_key="CANCEL", title="휴가 취소", message="{name}이(가) 휴가를 취소합니다.")  # 휴가 취소

    def test_푸시알림_가져오기_및_메시지생성(self):
        self.assertEqual(PushMessage.objects.count(), 4)
        message = PushMessage.get_message(push_key=PushMessage.PushType.CANCEL_BY_DRAFTER, name="paul")
        self.assertEqual("paul이(가) 휴가를 취소합니다.", message)
        message = PushMessage.get_message(push_key=PushMessage.PushType.CANCEL_BY_DRAFTER, name="daniel", test="test")
        self.assertEqual("daniel이(가) 휴가를 취소합니다.", message)
        message = PushMessage.get_message(push_key=PushMessage.PushType.DENY_BY_APPROVER, name="daniel", reason="지금 너무 바빠요.")
        self.assertEqual("daniel이(가) 휴가를 반려합니다. \n사유: 지금 너무 바빠요.", message)

