from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Profile


class AccountsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester",
            password="pass12345",
            email="tester@example.com",
        )

    def test_profile_created_by_signal(self):
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_profile_page_requires_login(self):
        response = self.client.get(reverse("profile_detail"))
        self.assertEqual(response.status_code, 302)

    def test_profile_page_loads_for_logged_in_user(self):
        self.client.login(username="tester", password="pass12345")
        response = self.client.get(reverse("profile_detail"))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_register_creates_user_and_profile(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "new_user",
                "email": "new_user@example.com",
                "first_name": "New",
                "last_name": "User",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )
        self.assertRedirects(response, reverse("profile_detail"))
        created_user = get_user_model().objects.get(username="new_user")
        self.assertTrue(Profile.objects.filter(user=created_user).exists())
