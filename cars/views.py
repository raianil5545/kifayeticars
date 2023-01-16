from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse

from .models import Car, CarImage, Location, Make, Model
from .forms import CarForm, AddCarImageForm

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if bool(u.groups.filter(name__in=group_names)):
            return True
        return False

    return user_passes_test(in_groups, login_url='/')


def cars_all(request):
    cars = Car.car_active_in_stock_objects.all()
    for car in cars:
        car_images_list = CarImage.objects.all().filter(car=car.id).values()
        images = [(index, image["car_image"]) for index, image in enumerate(car_images_list)]
        car.images = images
    return render(request, "cars/home.html", {"cars": cars})


def car_detail(request, slug):
    car = get_object_or_404(Car, slug=slug, in_stock=True)
    car_images = CarImage.objects.all().filter(car=car.id).values()
    images = [image["car_image"] for image in car_images]
    return render(request, "cars/single.html", {"car": car, "images": images})

def cars_by_location(request, location_slug):
    location = get_object_or_404(Location, slug=location_slug)
    cars = Car.objects.filter(location=location)
    for car in cars:
        car_images_list = CarImage.objects.all().filter(car=car.id).values()
        images = [image["car_image"] for image in car_images_list]
        car.images = images
    return render(request, "cars/home.html", {"cars" : cars})

def cars_by_make(request, make_slug):
    make = get_object_or_404(Make, slug=make_slug)
    cars = Car.objects.filter(make=make)
    for car in cars:
        car_image_list = CarImage.objects.all().filter(car=car.id).values()
        images = [image["car_image"] for image in car_image_list]
        car.images = images
        
    return render(request, "cars/home.html", {"cars" : cars})


@group_required("Staff")
def add_car(request):
    template = "cars/addcar.html"
    addform = CarForm()
    if request.method == "POST":
        make = Make.objects.get(brand=request.POST.get("make"))
        model = Model.objects.get(model=request.POST.get("model"))
        location =Location.objects.get(id=request.POST.get("location"))
        car = Car(
            user=request.user,
            price=request.POST.get("price"),
            year_of_manufacture=request.POST.get("year_of_manufacture"),
            max_customization_price=request.POST.get("max_customization_price"),
            description=request.POST.get("description"),
            make = make,
            model=model,
            location = location,
            slug = make.slug + "-" +  model.slug         
        )
        car.save()
        return redirect(reverse("cars:add_car_image", args=[car.slug]))
    context = {"form": addform}
    return render(request,template, context)

@group_required("Staff")
def add_car_image(request, car_slug):
    template = "cars/addcarimage.html"
    car_img_form = AddCarImageForm()
    if request.method == "POST":
        car = Car.objects.get(slug=car_slug)
        form = AddCarImageForm(request.POST, request.FILES)
        if form.is_valid():
            car_image = form.save(commit=False)
            car_image.car = car
            car_image.save()
            return redirect("/")
    context = {"form": car_img_form}
    return render(request,template, context)

@group_required("Staff")
def update_car(request, car_slug):
    obj = get_object_or_404(Car, slug = car_slug)
    context ={}
    form = CarForm(request.POST or None, instance = obj)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect("/")
        
    context["form"] = form
    template = "cars/updatecar.html"
    return render(request, template, context)


@group_required("Staff")
def delete_car(request, car_slug):
    template = "cars/403.html"
    car = Car.objects.get(slug=car_slug)
    if request.user == car.user:
        car.delete()
    else:
        return render(request, template)
    return redirect("/")


    