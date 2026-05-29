# Generated manually for custom user/profile lesson

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("username", models.CharField(error_messages={"unique": "A user with that username already exists."}, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.", max_length=150, unique=True, verbose_name="username")),
                ("first_name", models.CharField(blank=True, max_length=150, verbose_name="first name")),
                ("last_name", models.CharField(blank=True, max_length=150, verbose_name="last name")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="email address")),
                ("is_staff", models.BooleanField(default=False, help_text="Designates whether the user can log into this admin site.", verbose_name="staff status")),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
                ("bio", models.TextField(blank=True, verbose_name="Біо")),
                ("location", models.CharField(blank=True, max_length=120, verbose_name="Локація")),
                ("website", models.URLField(blank=True, verbose_name="Сайт")),
                ("github_profile", models.URLField(blank=True, verbose_name="GitHub")),
                ("linkedin_profile", models.URLField(blank=True, verbose_name="LinkedIn")),
                ("hourly_rate", models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name="Ставка/год")),
                ("is_available", models.BooleanField(default=True, verbose_name="Доступний для роботи")),
                ("phone", models.CharField(blank=True, max_length=30, verbose_name="Телефон")),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="customuser_set",
                        related_query_name="customuser",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="customuser_set",
                        related_query_name="customuser",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("avatar", models.ImageField(default="avatars/default_avatar.png", upload_to="avatars/", verbose_name="Аватар")),
                ("skills", models.TextField(blank=True, help_text="Напр. Python, Django, JS", verbose_name="Навички")),
                ("experience_years", models.PositiveIntegerField(default=0, verbose_name="Роки досвіду")),
                ("education", models.CharField(blank=True, max_length=200, verbose_name="Освіта")),
                ("languages", models.CharField(blank=True, max_length=100, verbose_name="Мови")),
                ("timezone", models.CharField(default="Europe/Kyiv", max_length=50, verbose_name="Часовий пояс")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to="accounts.customuser",
                        verbose_name="Користувач",
                    ),
                ),
            ],
            options={
                "verbose_name": "Профіль",
                "verbose_name_plural": "Профілі",
            },
        ),
    ]


