from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import StaffProfile, CustomerProfile

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertFalse(user.is_staff_member)
        self.assertFalse(user.is_customer)

    def test_create_staff_member(self):
        user = User.objects.create_user(
            username="staffuser", password="password", is_staff_member=True
        )
        self.assertTrue(user.is_staff_member)
        StaffProfile.objects.create(user=user, pay_rate=25.00)
        self.assertEqual(user.staff_profile.pay_rate, 25.00)

    def test_create_customer(self):
        user = User.objects.create_user(
            username="customeruser", password="password", is_customer=True
        )
        self.assertTrue(user.is_customer)
        CustomerProfile.objects.create(user=user, bond_amount=100.00)
        self.assertEqual(user.customer_profile.bond_amount, 100.00)


class AccountViewsTest(TestCase):
    def test_register_view_get(self):
        response = self.client.get("/accounts/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")
