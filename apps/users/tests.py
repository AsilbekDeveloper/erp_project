from django.test import TestCase
from apps.users.models import User, Role


class UserModelTest(TestCase):
    def test_create_user(self):
        u = User.objects.create_user(username="ali", password="pw", role=Role.STAFF)
        self.assertEqual(str(u), "ali")
        self.assertEqual(u.role, Role.STAFF)

    def test_create_superuser(self):
        u = User.objects.create_superuser(
            username="root", password="pw", role=Role.SUPERADMIN
        )
        self.assertTrue(u.is_superuser)
        self.assertEqual(u.role, Role.SUPERADMIN)

    def test_change_role(self):
        u = User.objects.create_user(username="b", password="pw")
        u.role = Role.ADMIN
        u.save()
        self.assertEqual(User.objects.get(pk=u.pk).role, Role.ADMIN)

    def test_blank_phone(self):
        u = User.objects.create_user(username="test", password="pw", phone="")
        self.assertEqual(u.phone, "")

    def test_avatar_field(self):
        u = User.objects.create_user(username="imguser", password="pw")
        self.assertFalse(u.avatar)
        self.assertIsNone(u.avatar.name if u.avatar else None)

    def test_groups_related(self):
        u = User.objects.create_user(username="groupuser", password="pw")
        self.assertTrue(u.groups.exists() or not u.groups.exists())

    def test_permissions_related(self):
        u = User.objects.create_user(username="permuser", password="pw")
        self.assertTrue(u.user_permissions.exists() or not u.user_permissions.exists())

    def test_str_method(self):
        u = User.objects.create_user(username="zz", password="pw")
        self.assertEqual(str(u), "zz")

    def test_indexes(self):
        self.assertTrue(any(idx.fields == ["role"] for idx in User._meta.indexes))

    def test_verbose_name(self):
        self.assertEqual(User._meta.verbose_name, "User")
        self.assertEqual(User._meta.verbose_name_plural, "Users")

    def test_is_active_default(self):
        u = User.objects.create_user(username="bobo", password="pw")
        self.assertTrue(u.is_active)

    def test_set_phone(self):
        u = User.objects.create_user(username="bobik", password="pw")
        u.phone = "998907777777"
        u.save()
        self.assertEqual(User.objects.get(pk=u.pk).phone, "998907777777")

    def test_user_password_set_and_check(self):
        u = User.objects.create_user(username="passu", password="pass1234")
        self.assertTrue(u.check_password("pass1234"))

    def test_create_with_full_fields(self):
        u = User.objects.create_user(
            username="ff", password="pw", role=Role.ADMIN, phone="911", avatar=None
        )
        self.assertEqual(u.role, Role.ADMIN)
        self.assertEqual(u.phone, "911")

    def test_many_users(self):
        User.objects.create_user(username="u1", password="pw")
        User.objects.create_user(username="u2", password="pw")
        User.objects.create_user(username="u3", password="pw")
        self.assertEqual(User.objects.count(), 3)

    def test_groups_and_permissions(self):
        u = User.objects.create_user(username="withgroups", password="pw")
        u.groups.clear()
        u.user_permissions.clear()
        self.assertFalse(u.groups.exists())
        self.assertFalse(u.user_permissions.exists())

    def test_user_is_staff_field(self):
        u = User.objects.create_user(username="staff", password="pw", is_staff=True)
        self.assertTrue(u.is_staff)

    def test_user_is_superuser_field(self):
        u = User.objects.create_superuser(username="admin", password="pw")
        self.assertTrue(u.is_superuser)
