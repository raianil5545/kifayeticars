from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class Test_Account_Views_Url(TestCase):
    def setUp(self) -> None:
        self.db = get_user_model()
        self.client = Client()
        self.credentials = {
            'email': 'some@gmail.com',
            'password': 'PWD123453'}
        return super().setUp()

    def tearDown(self) -> None:
        del self.db
        del self.client
        return super().tearDown()
