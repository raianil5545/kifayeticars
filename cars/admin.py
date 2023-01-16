from django.contrib import admin

from .models import Car, CarImage, Feedback, Location, Make, Model, Rating


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "price", "year_of_manufacture", "slug",
                    "max_customization_price", "make", "model",  "location", "is_active", "in_stock", "created"]
    list_filter = ["year_of_manufacture", "make", "model",  "location", "is_active", "in_stock"]
    list_editable = ["price", "is_active", "in_stock", "max_customization_price"]
    prepopulated_fields = {"slug": ("description",)}


@admin.register(Make)
class MakeAdmin(admin.ModelAdmin):
    list_display = ["id", "brand", "slug"]
    prepopulated_fields = {"slug": ("brand",)}


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ["id", "model", "slug", "make"]
    prepopulated_fields = {"slug": ("model",)}
    list_filter = ("make", )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "slug", "location")
    prepopulated_fields = {
        "slug": ("location", )
    }


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "comment", "car")
    list_filter = ("car", )


@admin.register(CarImage)
class CarImageAdmin(admin.ModelAdmin):
    list_display = ("id", "car_image", "car")
    list_filter = ("car", )


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "car", "star_ratings")
    list_filter = ("car", "star_ratings")
