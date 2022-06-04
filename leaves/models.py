from django.db import models


class Leave(models.Model):
    name = models.CharField(verbose_name="휴가 종류", max_length=30)
    consume = models.FloatField(verbose_name="소진일")

    def __str__(self):
        return f"{self.name} ({self.consume})"
