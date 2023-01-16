from django.urls import path

from . import views

app_name = "cars"


urlpatterns = [
    path("", views.cars_all, name="cars_all"),
    path("car/<slug:slug>", views.car_detail, name="car_detail"),
    path("cars/location/<slug:location_slug>", views.cars_by_location, name="cars_by_location"),
    path("cars/make/<slug:make_slug>", views.cars_by_make, name="cars_by_make"),
    path("cars/add", views.add_car, name="add_car"),
    path("cars/image/add/<slug:car_slug>", views.add_car_image, name="add_car_image"),
    path("car/update/<slug:car_slug>", views.update_car, name="update_car"),
    path("car/delete/<slug:car_slug>", views.delete_car, name="delete_car")
]
