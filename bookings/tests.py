from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Service, Booking
from pets.models import Pet
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password"
        )
        self.pet = Pet.objects.create(
            owner=self.user, name="Buddy", breed="Dog", age=3
        )
        self.service = Service.objects.create(name="Daycare", price=50.00)

    def test_create_booking(self):
        start = timezone.now()
        end = start + timedelta(hours=2)
        booking = Booking.objects.create(
            pet=self.pet,
            service=self.service,
            start_time=start,
            end_time=end,
            status="pending",
        )
        self.assertEqual(booking.pet.name, "Buddy")
        self.assertEqual(booking.service.name, "Daycare")


class BookingViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")

    def test_booking_list_view(self):
        response = self.client.get("/bookings/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/booking_list.html")
