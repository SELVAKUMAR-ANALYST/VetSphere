from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Pet, DailyLog

User = get_user_model()


class PetModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testowner", password="password"
        )

    def test_create_pet(self):
        pet = Pet.objects.create(
            owner=self.user, name="Buddy", breed="Golden Retriever", age=3
        )
        self.assertEqual(pet.name, "Buddy")
        self.assertEqual(pet.owner.username, "testowner")

    def test_daily_log(self):
        pet = Pet.objects.create(
            owner=self.user, name="Buddy", breed="Golden Retriever", age=3
        )
        log = DailyLog.objects.create(
            pet=pet,
            activity_type="walk",
            notes="Morning walk",
            logged_by=self.user,
        )
        self.assertEqual(log.activity_type, "walk")
        self.assertEqual(pet.daily_logs.count(), 1)


class PetViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password"
        )
        self.client.login(username="testuser", password="password")

    def test_pet_list_view(self):
        response = self.client.get("/pets/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pets/pet_list.html")
