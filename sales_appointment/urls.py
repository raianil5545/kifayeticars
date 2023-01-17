from django.urls import path

from . import views

app_name = "sales_appointment"

urlpatterns = [
    path('', views.appointment_summary, name='appointment_summary'),
    path('add', views.appointment_add, name='appointment_add'),
    path('delete', views.appointment_delete, name='appointment_delete'),
    path('update', views.appointment_update, name='appointment_update'),
]
