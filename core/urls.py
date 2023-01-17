from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("user/", include("account.urls")),
    path("", include("cars.urls", namespace="cars")),
    path("appointment/", include("sales_appointment.urls", namespace="sales_appointment"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
