from django.db import models


class PushMessage(models.Model):
    class PushType(models.TextChoices):
        APPROVE_BY_APPROVER = "APPROVE", "휴가수락"
        DENY_BY_APPROVER = "DENY", "휴가반려"
        REQUEST_BY_DRAFTER = "REQUEST", "휴가신청"
        CANCEL_BY_DRAFTER = "CANCEL", "휴가취소"

    push_key = models.CharField(max_length=20, choices=PushType.choices)
    title = models.CharField(max_length=100)
    message = models.TextField()

    @classmethod
    def get_message(cls, push_key, **kwargs):
        push_message = cls.objects.filter(push_key=push_key).first()
        push_message.message.format(**kwargs)
        return push_message.message.format(**kwargs)
