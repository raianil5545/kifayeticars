from cars.models import Car, CarImage


class Appointment():
    """
    A base Appointment class providing some default behaviors,
    that can be inherited or override, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        appointment = self.session.get('session_key')
        if 'session_key' not in self.session:
            appointment = self.session['session_key'] = {}
        self.appointment = appointment

    def add(self, car, appointment_date):
        """
        Adding and updating the car in appointment.
        """
        car_id = str(car.id)
        if car_id in self.appointment:
            self.appointment[car_id]['appointment_date'] = appointment_date
        else:
            self.appointment[car_id] = {'brand': str(car.make),
                                        'model': str(car.model),
                                        'base_price': str(car.price),
                                        'appointment_date': appointment_date,
                                        "appointment_number": 1}
        self.save()

    def __iter__(self):
        """
        collect the car_id in the session appoitment data to query the database and return cars
        """
        car_ids = self.appointment.keys()
        cars = Car.objects.filter(id__in=car_ids)
        appointment = self.appointment.copy()
        for car in cars:
            car_images_list = CarImage.objects.all().filter(car=car.id).values()
            images = [(index, image["car_image"]) for index, image in enumerate(car_images_list)]
            car.images = images
            appointment[str(car.id)]['car'] = car
        for item in appointment.values():
            yield item

    def __len__(self):
        """
        Get the appointment data and number
        """
        return sum(appointment["appointment_number"] for appointment in self.appointment.values())

    def delete(self, car):
        """
        Delete item from session data.
        """
        car_id = str(car)
        if car_id in self.appointment:
            del self.appointment[car_id]
            self.save()

    def update(self, car, appointment_date):
        """
        Update an appointment date
        """
        car_id = str(car)
        if car_id in self.appointment:
            self.appointment[car_id]['appointment_date'] = appointment_date
        self.save()

    def save(self):
        self.session.modified = True
