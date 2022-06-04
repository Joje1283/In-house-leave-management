from django.test import TestCase

from ..exceptions import NotFoundMember, DuplicateMember
from ..models import Member


class TestMemberManager(TestCase):
    def setUp(self) -> None:
        Member.objects.join(username="paul", password="test")
        Member.objects.join(username="daniel", password="test", approver_name="paul")

    def test_join(self):
        self.assertEqual(Member.objects.count(), 2)
        self.assertTrue(Member.objects.filter(username="paul").exists())
        self.assertTrue(Member.objects.filter(username="daniel").exists())

    def test_update_approver(self):
        daniel = Member.objects.get(username="daniel")
        Member.objects.join(username="john", password="test")
        self.assertEqual(daniel.approver.username, "paul")

        Member.objects.update_approver("daniel", "john")
        daniel = Member.objects.get(username="daniel")
        self.assertEqual(daniel.approver.username, "john")

    def test_get_or_validate_not_found_member(self):
        member = Member.objects.get_or_validate_not_found_member("paul")
        self.assertEqual(member.username, "paul")
        try:
            Member.objects.get_or_validate_not_found_member("test")
        except NotFoundMember:
            return
        self.fail()

    def test_validate_duplicate_member(self):
        try:
            Member.objects.validate_duplicate_member("paul")
        except DuplicateMember as e:
            return
        self.fail()
