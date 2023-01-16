from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from account.models import AppUser

from .constant import LOCATION_CHOICE


class CarActiveInstockManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, in_stock=True)


class Make(models.Model):
    brand = models.CharField(verbose_name="Brand Name", max_length=200, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    
    class Meta:
        verbose_name_plural = "makes"
        
    def __str__(self):
        return self.brand
    
    def get_absolute_url(self):
        return reverse("cars:cars_by_make", args=[self.slug])


class Model(models.Model):
    model = models.CharField(verbose_name="Car Model", max_length=150, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    make = models.ForeignKey(Make, on_delete=models.CASCADE, related_name="car_make")
    
    class Meta:
        verbose_name_plural = "models"
        
    def __str__(self):
        return self.model
    
class Location(models.Model):
    location = models.CharField(
        verbose_name="Show Room location",
        max_length=150,
        choices=LOCATION_CHOICE
    )
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "location"
        
    def __str__(self):
        return self.location
    
    def get_absolute_url(self):
        return reverse("cars:cars_by_location", args=[self.slug])

class Car(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="user")
    price = models.PositiveIntegerField(verbose_name="price")
    year_of_manufacture = models.CharField(verbose_name="year of manufacture", max_length=150)
    max_customization_price = models.PositiveIntegerField(verbose_name="Maximum amount for customization")
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    make = models.ForeignKey(Make, on_delete=models.CASCADE, related_name="make", to_field="brand")
    model = models.OneToOneField(Model, on_delete=models.CASCADE, related_name="car_model", to_field="model")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="carlocation")
    slug = models.SlugField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    car_active_in_stock_objects = CarActiveInstockManager()
    
    class Meta:
        verbose_name_plural = "cars"
        ordering = ("-created", )
    
    def get_absolute_url(self):
        return reverse("cars:car_detail", args=[self.slug])
    
    def get_absolute_url_update(self):
        return reverse("cars:update_car", args=[self.slug])
    
    def get_car_image_absolute_url(self):
        return reverse("cars:add_car_image", args=[self.slug])
    
    def get_car_delete_absolute_url(self):
        return reverse("cars:delete_car", args=[self.slug])
         

class Feedback(models.Model):
    comment = models.TextField(verbose_name="Customer Comment")
    car = models.ForeignKey(Car, 
                            on_delete=models.CASCADE,
                            verbose_name="car id")
    


class Rating(models.Model):
    star_ratings = models.SmallIntegerField(verbose_name="rating star",
                                            validators=(MinValueValidator(0), MaxValueValidator(5)))
    car = models.ForeignKey(Car, 
                            on_delete=models.CASCADE,
                            verbose_name="car id")


class CarImage(models.Model):
    car_image = models.ImageField(upload_to="images/")
    car = models.ForeignKey(Car, 
                            on_delete=models.CASCADE,
                            verbose_name="car id")
    
    

    