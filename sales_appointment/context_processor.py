from .appointment import Appointment


def appointment(request):
    return {'appointment': Appointment(request)}
