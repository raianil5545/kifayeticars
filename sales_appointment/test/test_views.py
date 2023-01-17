from django.contrib.auth.models import Group
from django.test import Client, TestCase
from django.urls import reverse

from account.models import AppUser
from cars.models import Car, Location, Make, Model


class TestAppointmentView(TestCase):
    def setUp(self):
        self.client = Client()
        self.location = Location.objects.create(location="kathmandu", slug="kathmandu")
        self.make1 = Make.objects.create(brand="Honda", slug="honda")
        self.model1 = Model.objects.create(model="civic", slug="civic", make=self.make1)
        self.make2 = Make.objects.create(brand="Tata", slug="tata")
        self.model2 = Model.objects.create(model="sumo", slug="sumo", make=self.make2)
        self.consumer_group = Group.objects.get_or_create(name="Customer")
        self.user = AppUser(
            first_name="test",
            last_name="rest",
            email="test_rest5545@gmail.com"
        )
        self.user.set_password("somepwd")
        self.user.save()
        self.new_user = AppUser.object.get(email=self.user.email)
        self.new_user.groups.add(self.consumer_group[0])
        self.new_user.save()
        self.client.login(email="test_rest5545@gmail.com", password="somepwd")
        self.car_1 = Car.objects.create(user=self.user,
                                        price=100000,
                                        year_of_manufacture=2018,
                                        max_customization_price=50000,
                                        description="first car",
                                        make=self.make1,
                                        model=self.model1,
                                        location=self.location,
                                        slug="firstcar")
        self.car_2 = Car.objects.create(user=self.user,
                                        price=200000,
                                        year_of_manufacture=2019,
                                        max_customization_price=70000,
                                        description="second car",
                                        make=self.make2,
                                        model=self.model2,
                                        location=self.location,
                                        slug="secondcar")

    def test_appointment_url(self):
        """
        Test home page response status
        """
        response = self.client.get(reverse('sales_appointment:appointment_summary'))
        self.assertEqual(response.status_code, 200)

    def test_appointment_add(self):
        """
        Testing appoint added
        """
        response = self.client.post(
            reverse('sales_appointment:appointment_add'),
            {"carid": self.car_1.id, "appointment_date": "2017-08-20", "action": "post"}, xhr=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"appointment_number": 1})
        response = self.client.post(
            reverse('sales_appointment:appointment_add'),
            {"carid": self.car_2.id, "appointment_date": "2017-08-21", "action": "post"}, xhr=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"appointment_number": 2})

    def test_appointment_delete(self):
        """
        Testing appoint added
        """
        self.client.post(
            reverse('sales_appointment:appointment_add'),
            {"carid": self.car_1.id, "appointment_date": "2017-08-20", "action": "post"}, xhr=True)
        self.client.post(
            reverse('sales_appointment:appointment_add'),
            {"carid": self.car_2.id, "appointment_date": "2017-08-21", "action": "post"}, xhr=True)
        response = self.client.post(
            reverse('sales_appointment:appointment_delete'),
            {"carid": self.car_2.id, "action": "post"}, xhr=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"appointment_number": 1})

    def test_appointment_update(self):
        self.client.post(
            reverse('sales_appointment:appointment_add'),
            {"carid": self.car_1.id, "appointment_date": "2017-08-20", "action": "post"}, xhr=True)
        response = self.client.post(
            reverse('sales_appointment:appointment_update'),
            {"carid": self.car_2.id, "appointment_date": "2018-09-21", "action": "post"}, xhr=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"appointment_date": "2018-09-21"})
