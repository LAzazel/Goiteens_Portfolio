from django.test import TestCase


class PortfolioSmokeTests(TestCase):
    def test_home_view_loads(self):
        response = self.client.get("/")
        self.assertIn(response.status_code, {200, 302})

