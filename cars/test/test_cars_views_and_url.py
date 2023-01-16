from django.conf import settings
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from account.models import AppUser
from cars.models import Car, Location, Make, Model
from cars.views import cars_all

User = settings.AUTH_USER_MODEL


class TestCarsViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.location = Location.objects.create(location="kathmandu", slug="kathmandu")
        self.make = Make.objects.create(brand="Honda", slug="honda")
        self.model = Model.objects.create(model="civic", slug="civic", make=self.make)
        self.user = AppUser(
            first_name="test",
            last_name="rest",
            password="somepwd",
            email="test_rest5545@gmail.com"
        )
        self.user.save()
        self.car = Car.objects.create(user=self.user,
                                      price=100000,
                                      year_of_manufacture=2018,
                                      max_customization_price=50000,
                                      description="some thing",
                                      make=self.make,
                                      model=self.model,
                                      location=self.location,
                                      slug="someslug")

    def tearDown(self) -> None:
        self.user.delete()
        self.model.delete()
        self.make.delete()
        self.location.delete()
        self.car.delete()
        return super().tearDown()

    def test_home_page_url_status_code(self):
        """
        testing the home page functionality
        """
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_html(self):
        request = HttpRequest()
        response = cars_all(request)
        html = response.content.decode("utf-8")
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn("Home", html)

    def test_car_detail_url_status_code_200(self):
        respone = self.client.get(reverse("cars:car_detail", args=["someslug"]))
        self.assertEqual(respone.status_code, 200)

    def test_car_detail_url_status_code_404(self):
        respone = self.client.get(reverse("cars:car_detail", args=["invalidslug"]))
        self.assertEqual(respone.status_code, 404)

    def test_car_by_location_url_status_code_200(self):
        respone = self.client.get(
            reverse("cars:cars_by_location", args=["kathmandu"])
        )
        self.assertEqual(respone.status_code, 200)

    def test_car_by_location_url_status_code_404(self):
        respone = self.client.get(
            reverse("cars:cars_by_location", args=["invalidlocation"])
        )
        self.assertEqual(respone.status_code, 404)

    def test_view_function(self):
        request = self.factory.get("cars/1/")
        response = cars_all(request)
        html = response.content.decode("utf-8")
        self.assertIn("Honda civic", html)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertEqual(response.status_code, 200)

    def test_url_allowed_hosts(self):
        """
        Test allowed host
        """
        response = self.client.get("/", HTTP_HOST="noaddress.com")
        self.assertEqual(response.status_code, 400)
        response = self.client.get("/", HTTP_HOST="yourdomain.com")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/", HTTP_HOST="127.0.0.1")
        self.assertEqual(response.status_code, 200)
