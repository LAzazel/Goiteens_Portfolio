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
