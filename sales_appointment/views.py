from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from auth.group_permission import group_required
from cars.models import Car

from .appointment import Appointment


@group_required("Customer")
def appointment_summary(request):
    appointment = Appointment(request)
    return render(request, "sales/appointment/summary.html", {'appointment': appointment})


@group_required("Customer")
def appointment_add(request):
    appointment = Appointment(request)
    if request.POST.get('action') == 'post':
        car_id = int(request.POST.get('carid'))
        appointment_date = str(request.POST.get('appointment_date'))
        car = get_object_or_404(Car, id=car_id)
        appointment.add(car=car, appointment_date=appointment_date)
        appointment_number = appointment.__len__()
        response = JsonResponse({"appointment_number": appointment_number})
        return response


@group_required("Customer")
def appointment_delete(request):
    appointment = Appointment(request)
    if request.POST.get('action') == 'post':
        car_id = int(request.POST.get('carid'))
        appointment.delete(car=car_id)
        appointment_number = appointment.__len__()
        response = JsonResponse({"appointment_number": appointment_number})
        return response


@group_required("Customer")
def appointment_update(request):
    appointment = Appointment(request)
    if request.POST.get('action') == 'post':
        car_id = int(request.POST.get('carid'))
        appointment_date = str(request.POST.get('appointment_date'))
        appointment.update(car_id, appointment_date)
        response = JsonResponse({"appointment_date": appointment_date})
        return response
