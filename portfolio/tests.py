from django.test import TestCase
from django.urls import reverse
from django.test import override_settings
from django.utils import timezone
from .models import Order, Project, Review
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


class ReviewTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            title="Test project",
            description="Description",
            technologies="Django, Bootstrap",
            created_at=timezone.now().date(),
        )

    def test_review_form_renders(self):
        response = self.client.get(reverse("project_detail", args=[self.project.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Залишити відгук")

    def test_review_post_creates_hidden_review_and_redirects(self):
        response = self.client.post(
            reverse("project_detail", args=[self.project.pk]),
            {
                "client_name": "Olha",
                "text": "Great work",
                "rating": 5,
            },
        )
        self.assertRedirects(response, f"{reverse('project_detail', args=[self.project.pk])}?review=sent")
        review = Review.objects.get(project=self.project)
        self.assertFalse(review.visible)
        self.assertEqual(review.client_name, "Olha")
        self.assertEqual(review.text, "Great work")

    def test_reviews_list_shows_only_visible_reviews(self):
        visible_review = Review.objects.create(
            client_name="Anna",
            text="Nice job",
            rating=5,
            project=self.project,
            visible=True,
        )
        Review.objects.create(
            client_name="Hidden",
            text="Should not show",
            rating=1,
            project=self.project,
            visible=False,
        )

        response = self.client.get(reverse("reviews_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, visible_review.client_name)
        self.assertContains(response, visible_review.text)
        self.assertNotContains(response, "Should not show")


