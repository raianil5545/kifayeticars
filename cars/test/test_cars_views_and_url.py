from importlib import import_module
from io import BytesIO

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest, HttpResponseRedirect
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse
from PIL import Image

from account.models import AppUser
from cars.models import Car, Location, Make, Model
from cars.views import cars_all

User = settings.AUTH_USER_MODEL


def temporary_image():
    bts = BytesIO()
    img = Image.new("RGB", (100, 100))
    img.save(bts, 'jpeg')
    return SimpleUploadedFile("test.jpg", bts.getvalue())


class TestCarsViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.location = Location.objects.create(location="kathmandu", slug="kathmandu")
        self.make = Make.objects.create(brand="Honda", slug="honda")
        self.model = Model.objects.create(model="civic", slug="civic", make=self.make)
        self.user = AppUser.objects.create_user(
            first_name="staff",
            last_name="one",
            email="staff1@kifayeticar.com",
            password="Staff1@",
            is_staff=True,
        )
        self.user.is_active = True
        staff_group = Group.objects.get_or_create(name="Staff")
        self.user.groups.add(staff_group[0])
        self.user.save()
        credentials = {
            'username': 'staff1@kifayeticar.com',
            'password': 'Staff1@'}
        self.client.post(reverse('account:login'), credentials)
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
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
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

    def test_car_by_nake_url_status_code_200(self):
        respone = self.client.get(
            reverse("cars:cars_by_make", args=["honda"])
        )
        self.assertEqual(respone.status_code, 200)

    def test_car_by_nake_url_status_code_400(self):
        respone = self.client.get(
            reverse("cars:cars_by_make", args=["invalid"])
        )
        self.assertEqual(respone.status_code, 404)

    def test_view_function(self):
        request = self.factory.get("cars/1/")
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()
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

    def test_add_car_with_staff_group(self):
        location = Location.objects.create(location="pokhara", slug="pokhara")
        make = Make.objects.create(brand="Tata", slug="tata")
        model = Model.objects.create(model="sumo", slug="sumo", make=self.make)
        data = dict(
            price=5000000,
            year_of_manufacture=2018,
            max_customization_price=700000,
            description="some text here",
            make=make,
            model=model,
            location=location.id)
        response = self.client.post(reverse('cars:add_car'), data=data)
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_add_car_get_form_with_staff_group(self):
        response = self.client.get(reverse('cars:add_car'))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode("utf-8")
        self.assertIn('Add Car', html)
        self.assertIn("<h1>Add Cars Page</h1>", html)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))

    def test_update_car_render_html_with_staff_group(self):
        response = self.client.get(reverse('cars:update_car', args=[self.car.slug]))
        self.assertEqual(response.status_code, 200)
        html = response.content.decode("utf-8")
        self.assertIn('Update Car', html)
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn("Honda", html)
        self.assertIn("civic", html)
        self.assertIn("2018", html)

    def test_update_car_and_redirect_with_staff_group(self):
        location = Location.objects.create(location="pokhara", slug="pokhara")
        make = Make.objects.create(brand="Tata", slug="tata")
        model = Model.objects.create(model="sumo", slug="sumo", make=self.make)
        data = dict(
            price=5000000,
            year_of_manufacture=2018,
            max_customization_price=700000,
            description="some text here",
            make=make,
            model=model,
            location=location.id)
        response = self.client.post(reverse('cars:update_car', args=[self.car.slug]), data)
        self.assertIsInstance(response, HttpResponseRedirect)
        response = self.client.get(reverse('cars:update_car', args=[self.car.slug]))
        html = response.content.decode("utf-8")
        self.assertIn("Tata", html)
        self.assertIn("sumo", html)
        self.assertIn("2018", html)

    def test_add_car_image_redirect(self):
        response = self.client.post(reverse('cars:add_car_image', args=[self.car.slug]),
                                    {'car_image': temporary_image()}, format="multipart")
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_render_add_car_image_template(self):
        response = self.client.get(reverse('cars:add_car_image', args=[self.car.slug]))
        html = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Add Car Image", html)

    def test_redirect_car_delete(self):
        response = self.client.get(reverse('cars:delete_car', args=[self.car.slug]))
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_render_403_car_delete(self):
        self.user2 = AppUser.objects.create_user(
            first_name="staff",
            last_name="one",
            email="staff2@kifayeticar.com",
            password="Staff2@",
            is_staff=True,
        )
        self.user2.is_active = True
        staff_group = Group.objects.get_or_create(name="Staff")
        self.user2.groups.add(staff_group[0])
        self.user2.save()
        credentials = {
            'username': 'staff2@kifayeticar.com',
            'password': 'Staff2@'}
        self.client.post(reverse('account:login'), data=credentials)
        response = self.client.get(reverse('cars:delete_car', args=[self.car.slug]))
        html = response.content.decode('utf-8')
        self.assertIn('Permission denied', html)
        self.assertEqual(response.status_code, 200)
