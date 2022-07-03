import sentry_sdk
from celery import shared_task

from members.models import Member

"""
# 실행 방법 예시 (shell)

from datetime import datetime, timedelta
from push.tasks import push_print

push_print.apply_async(["안녕하세요 폴222"], eta=datetime.now() + timedelta(seconds=10), queue="paul_worker")
"""


@shared_task
def push_print(s):
    print(s)


@shared_task
def send_welcome_email(username: str):
    try:
        member = Member.objects.get(username=username)
        member.send_welcome_email()
    except Exception as e:
        sentry_sdk.capture_exception(e)
