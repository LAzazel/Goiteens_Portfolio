from django.shortcuts import render

from .models import Experience, Project, Skill


def home(request):
    projects = Project.objects.order_by("-created_at")[:6]
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    return render(
        request,
        "home.html",
        {
            "projects": projects,
            "skills": skills,
            "experiences": experiences,
        },
    )

