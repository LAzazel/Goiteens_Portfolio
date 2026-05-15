from django.contrib import admin

from .models import Experience, Project, ProjectImage, Skill


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
