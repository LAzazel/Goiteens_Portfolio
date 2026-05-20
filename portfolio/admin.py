from django.contrib import admin

from .models import Experience, Project, ProjectImage, Skill
from .models import Order, Review


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "technologies")
    search_fields = ("title", "technologies")
    list_filter = ("created_at",)
    inlines = [ProjectImageInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "category")
    list_filter = ("category",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("position", "company", "period")
    search_fields = ("position", "company")



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "client_name", "client_email", "budget", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "client_name", "client_email", "description")
    readonly_fields = ("created_at",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("client_name", "rating", "project", "visible", "created_at")
    list_filter = ("visible", "rating")
    search_fields = ("client_name", "text")

