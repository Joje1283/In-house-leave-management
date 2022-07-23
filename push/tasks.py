import sentry_sdk
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string

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
        print("start send_welcome_email")
        member = Member.objects.get(username=username)
        print(f"{member.username}에게 메일을 보냅니다.")
        result = member.send_welcome_email()
        print(result)
    except Exception as e:
        sentry_sdk.capture_exception(e)


@shared_task
def send_email_push(from_address, to_address_list, subject, content):
    return send_mail(subject, content, from_address, [to_address_list], fail_silently=False)
