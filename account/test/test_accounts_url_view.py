from django.http import HttpResponseRedirect
from django.test import Client, TestCase
from django.urls import reverse

from account.models import AppUser


class Test_Account_Views_Url(TestCase):
    def setUp(self):
        self.client = Client()

    def tearDown(self):
        del self.client
        return super().tearDown()

    def test_register_user_customer(self):
        user = dict(
            email="some@gmail.com",
            first_name="customer",
            last_name="one",
            password="PWD123453"
        )
        response = self.client.post(reverse('account:register'), data=user)
        self.assertIsInstance(response, HttpResponseRedirect)
        user = AppUser.object.get(email="some@gmail.com")
        user_customer = user.groups.filter(name='Customer').exists()
        self.assertTrue(user_customer)
        self.assertEqual(user.id, 1)

    def test_register_user_staff(self):
        user = dict(
            email="staff@kifayeticar.com",
            first_name="staff",
            last_name="one",
            password="Staff123453"
        )
        response = self.client.post(reverse('account:register'), data=user)
        self.assertIsInstance(response, HttpResponseRedirect)
        user = AppUser.object.get(email="staff@kifayeticar.com")
        staff_customer = user.groups.filter(name='Staff').exists()
        self.assertTrue(staff_customer)
        self.assertEqual(user.id, 1)

    def test_user_login_success_url(self):
        user = dict(
            email="some@gmail.com",
            first_name="customer",
            last_name="one",
            password="PWD123453"
        )
        self.client.post(reverse('account:register'), data=user)
        credentials = {
            'username': 'some@gmail.com',
            'password': 'PWD123453'}
        response = self.client.post(reverse('account:login'), data=credentials, follow=True)
        session = self.client.session
        self.assertEqual(session.get("user_email"), "some@gmail.com")
        self.assertFalse(session.get("is_staff"))
        self.assertEqual(session.get("user_id"), 1)
        self.assertEqual(response.status_code, 200)

    def test_user_logout_success_url(self):
        user = dict(
            email="some@gmail.com",
            first_name="customer",
            last_name="one",
            password="PWD123453"
        )
        self.client.post(reverse('account:register'), data=user)
        credentials = {
            'username': 'some@gmail.com',
            'password': 'PWD123453'}
        self.client.post(reverse('account:login'), data=credentials, follow=True)
        session = self.client.session
        self.client.post(reverse('account:logout'))
        self.assertEqual(session.get("user_email"), None)
        self.assertEqual(session.get("user_id"), None)
        self.assertEqual(session.get("is_staff"), None)
