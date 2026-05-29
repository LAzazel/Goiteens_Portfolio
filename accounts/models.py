import os
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    """Custom user model for freelancer profile data."""

    bio = models.TextField(blank=True, verbose_name="Біо")
    location = models.CharField(max_length=120, blank=True, verbose_name="Локація")
    website = models.URLField(blank=True, verbose_name="Сайт")
    github_profile = models.URLField(blank=True, verbose_name="GitHub")
    linkedin_profile = models.URLField(blank=True, verbose_name="LinkedIn")
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Ставка/год")
    is_available = models.BooleanField(default=True, verbose_name="Доступний для роботи")
    phone = models.CharField(max_length=30, blank=True, verbose_name="Телефон")

    def __str__(self):
        return self.username


class Profile(models.Model):
    """User profile with avatar and extended information."""

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="profile", verbose_name="Користувач")
    avatar = models.ImageField(default="avatars/default_avatar.png", upload_to="avatars/", verbose_name="Аватар")
    skills = models.TextField(blank=True, help_text="Напр. Python, Django, JS", verbose_name="Навички")
    experience_years = models.PositiveIntegerField(default=0, verbose_name="Роки досвіду")
    education = models.CharField(max_length=200, blank=True, verbose_name="Освіта")
    languages = models.CharField(max_length=100, blank=True, verbose_name="Мови")
    timezone = models.CharField(max_length=50, default="Europe/Kyiv", verbose_name="Часовий пояс")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Профіль"
        verbose_name_plural = "Профілі"

    def __str__(self):
        return f"Профіль {self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.avatar and hasattr(self.avatar, "path") and os.path.exists(self.avatar.path):
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                img.thumbnail((300, 300))
                img.save(self.avatar.path)

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(",") if s.strip()] if self.skills else []


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "profile"):
        instance.profile.save()

