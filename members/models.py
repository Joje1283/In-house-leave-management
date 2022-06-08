from __future__ import annotations

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from members.exceptions import NotFoundMember, DuplicateMember
from grants.models import Grant


class MemberManager(UserManager):
    def join(self, username: str, password: str, approver_name: str = None):
        self.validate_duplicate_member(username)
        approver = None
        if approver_name:
            approver = self.get_or_validate_not_found_member(username=approver_name)
        new_member = self.model(username=username, approver=approver)
        new_member.set_password(password)
        new_member.save()

    def update_approver(self, username: str, approver_name: str):
        approver = self.get_or_validate_not_found_member(username=approver_name)
        target_member = self.get_or_validate_not_found_member(username=username)
        target_member.approver = approver
        target_member.save()

    def get_or_validate_not_found_member(self, username: str):
        member = self.filter(username=username).first()
        if not member:
            raise NotFoundMember(f"멤버를 찾을 수 없습니다. {username}")
        return member

    def validate_duplicate_member(self, username: str):
        if self.filter(username=username).exists():
            raise DuplicateMember("이미 존재하는 회원입니다.")


class Member(AbstractUser):
    approver = models.ForeignKey(verbose_name="결재자", to="self", on_delete=models.DO_NOTHING, null=True, blank=True)

    objects = MemberManager()

    def granted_leave_count(self):
        return Grant.objects.granted_stock(username=self.username)
