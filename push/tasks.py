from celery import shared_task


@shared_task
def push_print(s):
    print(s)
