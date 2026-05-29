from django.urls import path, include

from .views import profile_detail, profile_edit, register

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", register, name="register"),
    path("profile/", profile_detail, name="profile_detail"),
    path("profile/edit/", profile_edit, name="profile_edit"),
]
