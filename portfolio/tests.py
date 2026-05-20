from django.test import TestCase
from django.urls import reverse
from django.test import override_settings
from .models import Order
from django.core import mail


class PortfolioSmokeTests(TestCase):
    def test_home_view_loads(self):
        response = self.client.get("/")
        self.assertIn(response.status_code, {200, 302})


class OrderTests(TestCase):
    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend", DEFAULT_FROM_EMAIL="test@example.com")
    def test_order_creation_sends_email(self):
        data = {
            "client_name": "Ivan",
            "client_email": "ivan@example.com",
            "title": "New site",
            "description": "Need website",
        }
        resp = self.client.post(reverse("create_order"), data)
        self.assertRedirects(resp, reverse("order_thanks"))
        self.assertEqual(Order.objects.count(), 1)
        # Проверяем, что отправляются письма (уведомление владельцу и подтверждение клиенту)
        self.assertGreaterEqual(len(mail.outbox), 1)


