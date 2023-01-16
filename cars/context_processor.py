from .models import Location, Make


def locations(request):
    return {
        'locations': Location.objects.all()
    }

def makes(request):
    return {
        'makes': Make.objects.all()
    }