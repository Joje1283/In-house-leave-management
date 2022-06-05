from django.test import TestCase
from ..models import Leave


class TestLeave(TestCase):
    def setUp(self) -> None:
        Leave.objects.create(name="연차", consume=1)
        Leave.objects.create(name="반차", consume=0.5)
        Leave.objects.create(name="무급휴가", consume=0)

    def test_leave_create(self):
        self.assertEqual(3, Leave.objects.count())
        data = Leave.objects.get(name="연차")
        self.assertEqual(1, data.consume)

        data = Leave.objects.get(name="반차")
        self.assertEqual(0.5, data.consume)

        data = Leave.objects.get(name="무급휴가")
        self.assertEqual(0, data.consume)

    def test_leave_delete(self):
        data = Leave.objects.get(name="연차")
        data.delete()
        self.assertEqual(None, Leave.objects.filter(name="연차").first())

