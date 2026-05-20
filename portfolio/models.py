from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    technologies = models.CharField(
        max_length=255,
        help_text="Напр.: Django, PostgreSQL, Bootstrap",
    )
    created_at = models.DateField()
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="projects/gallery/")
    caption = models.CharField(max_length=140, blank=True)

    def __str__(self):
        return f"{self.project.title} image"


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("backend", "Backend"),
        ("frontend", "Frontend"),
        ("devops", "DevOps"),
        ("other", "Other"),
    ]
    name = models.CharField(max_length=80)
    level = models.PositiveSmallIntegerField(help_text="0-100")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")

    def __str__(self):
        return f"{self.name} ({self.level}%)"


class Experience(models.Model):
    position = models.CharField(max_length=120)
    company = models.CharField(max_length=120)
    period = models.CharField(max_length=120, help_text="Напр.: 2022-2024")
    description = models.TextField()

    def __str__(self):
        return f"{self.position} @ {self.company}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("in_progress", "In progress"),
        ("completed", "Completed"),
        ("rejected", "Rejected"),
    ]

    client_name = models.CharField(max_length=120)
    client_email = models.EmailField()
    client_phone = models.CharField(max_length=40, blank=True)
    title = models.CharField(max_length=200, help_text="Короткий заголовок проєкту")
    description = models.TextField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    processed_by = models.ForeignKey("auth.User", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk} - {self.title} ({self.client_name})"


class Review(models.Model):
    client_name = models.CharField(max_length=120)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, help_text="1-5")
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review by {self.client_name} ({self.rating})"

