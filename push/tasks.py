from celery import shared_task

"""
# 실행 방법 예시 (shell)

from datetime import datetime, timedelta
from push.tasks import push_print

push_print.apply_async(["안녕하세요 폴222"], eta=datetime.now() + timedelta(seconds=10), queue="paul_worker")
"""


@shared_task
def push_print(s):
    print(s)
