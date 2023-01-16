import tempfile
from io import BytesIO

from django.test import TestCase
from django.urls import reverse
from PIL import Image

from account.models import AppUser
from cars.models import Car, CarImage, Feedback, Location, Make, Model, Rating


class TestBase(TestCase):
    def setUp(self):
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
        return super().setUp()

    def tearDown(self) -> None:
        self.user.delete()
        self.model.delete()
        self.make.delete()
        self.location.delete()
        self.car.delete()
        return super().tearDown()


class TestLocationModel(TestCase):
    def setUp(self):
        self.location1 = Location.objects.create(location="kathmandu", slug="kathmandu")
        
    def tearDown(self) -> None:
        self.location1.delete()
        
    def test_location_model_entry(self):
        data = self.location1
        self.assertTrue(isinstance(data, Location))
        self.assertEqual(str(data), "kathmandu")
        self.assertEqual(data.slug, "kathmandu")
        # inserted first record
        self.assertAlmostEqual(data.id, 1)

        
    
    def test_location_reverse_url(self):
        data = self.location1
        self.assertEqual(data.get_absolute_url(), "/cars/location/kathmandu")



class TestMakeModel(TestCase):
    def setUp(self) -> None:
        self.make = Make.objects.create(brand="Honda", slug="honda")
        return super().setUp()

    def tearDown(self) -> None:
        self.make.delete()
        return super().tearDown()
    
    def test_make_model_entry(self):
        data = self.make
        self.assertTrue(isinstance(data, Make))
        self.assertAlmostEqual(str(data), "Honda")
        self.assertEqual(data.slug, "honda")
        self.assertAlmostEqual(data.id, 1)


class TestModelModel(TestCase):
    def setUp(self) -> None:
        self.make = Make.objects.create(brand="Honda", slug="honda")
        self.model = Model.objects.create(model="civic", slug="civic", make=self.make)
        return super().setUp()
    
    def tearDown(self) -> None:
        self.model.delete()
        self.make.delete()
        return super().tearDown()

    def test_model_entry(self):
        data = self.model
        self.assertIsInstance(data, Model)
        self.assertEqual(str(data), "civic")
        self.assertEqual(data.slug, "civic")
        self.assertAlmostEqual(data.id, 1)



class TestcarModel(TestBase):
    def test_car_created_in_models(self):
        data = self.car
        
        self.assertIsInstance(data, Car)
        self.assertEqual(data.price, 100000)
        self.assertEqual(data.year_of_manufacture, 2018)
        self.assertEqual(data.max_customization_price, 50000)
        self.assertEqual(data.user, self.user)
        self.assertEqual(data.model, self.model)
        self.assertEqual(data.is_active, True)
        self.assertEqual(data.in_stock, True)
        
        
    def test_car_model_get_absolute_url(self):
        self.assertEqual(self.car.get_absolute_url(), f"/car/{self.car.slug}")
        
    
class TestFeedBackModel(TestBase):  
    def test_feedback_model_entry(self):
        data = Feedback.objects.create(car=self.car, comment="some cmt")
        self.assertIsInstance(data, Feedback)
        self.assertEqual(data.comment, "some cmt")
        

class TestRatingModel(TestBase):
    def test_rating_model_data_entry_pass(self):
        data = Rating.objects.create(car=self.car, star_ratings=4)
        
        self.assertIsInstance(data, Rating)
        self.assertEqual(data.star_ratings, 4)

        
    
    
    