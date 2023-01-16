from django import forms

from .models import Car, CarImage


class CarForm(forms.ModelForm):
    class Meta:
        fields = ("price", "year_of_manufacture",
                  "max_customization_price", "description",
                  "make", "model",
                  "location")
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control w-50'}),
            'year_of_manufacture': forms.TextInput(attrs={'class': 'form-control w-50'}),
            'max_customization_price': forms.NumberInput(attrs={'class': 'form-control w-50'}),
            'description': forms.Textarea(attrs={'class': 'form-control w-50'}),
            'make': forms.Select(attrs={'class': 'form-control w-50'}),
            'model': forms.Select(attrs={'class': 'form-control w-50'}),
            'location': forms.Select(attrs={'class': 'form-control w-50'})
        }

        model = Car


class AddCarImageForm(forms.ModelForm):
    class Meta:
        fields = ("car_image",)
        widgets = {
            "car_image": forms.FileInput(attrs={'class': 'form-control w-50'})
            }
        model = CarImage
