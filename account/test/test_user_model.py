import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase


class TestUserAccount(TestCase):
    def setUp(self) -> None:
        self.db = get_user_model()
        return super().setUp()

    def tearDown(self) -> None:
        del self.db
        return super().tearDown()

    @pytest.mark.django_db
    def test_new_super_user(self):
        super_user = self.db.objects.create_superuser(
            "test_super@gmail.com", "first_name", "last_name", "pwd1234"
        )
        self.assertEqual(super_user.email, "test_super@gmail.com")
        self.assertEqual(super_user.first_name, "first_name")
        self.assertEqual(super_user.last_name, "last_name")
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), "test_super@gmail.com")

    @pytest.mark.django_db
    def test_new_user(self):
        user = self.db.objects.create_user(
                                         first_name="first name",
                                         last_name="last name",
                                         email="some@gmail.com",
                                         password="PWD123453"
        )
        self.assertEqual(user.email,  "some@gmail.com")
        self.assertEqual(user.first_name, "first name")
        self.assertEqual(user.last_name, "last name")
        self.assertEqual(user.is_staff, False)
        self.assertFalse(user.is_superuser)
        with self.assertRaises(ValueError):
            self.db.objects.create_user(
                                      first_name="first name",
                                      last_name="last name",
                                      email="",
                                      password="PWD123453")

        with self.assertRaises(ValueError):
            self.db.objects.create_user(
                                       first_name="",
                                       last_name="last name",
                                       email="some@gmail.com",
                                       password="PWD123453")
