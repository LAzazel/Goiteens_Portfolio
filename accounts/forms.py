from zoneinfo import available_timezones

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser, Profile


TIMEZONE_CHOICES = sorted(
    [(tz, tz) for tz in available_timezones() if tz.startswith("Europe/")],
    key=lambda item: item[0],
)
if ("Europe/Kyiv", "Europe/Kyiv") not in TIMEZONE_CHOICES:
    TIMEZONE_CHOICES.insert(0, ("Europe/Kyiv", "Europe/Kyiv"))


class CustomUserCreationForm(UserCreationForm):
    """Admin form for creating custom users."""

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class CustomUserChangeForm(UserChangeForm):
    """Admin form for updating custom users."""

    class Meta:
        model = CustomUser
        fields = "__all__"


class ProfileUpdateForm(forms.ModelForm):
    """Form for profile updates."""

    class Meta:
        model = Profile
        fields = ["avatar", "skills", "experience_years", "education", "languages", "timezone"]
        widgets = {
            "avatar": forms.FileInput(attrs={"class": "form-control", "accept": "image/*"}),
            "skills": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Python, Django, JS..."}
            ),
            "experience_years": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "education": forms.TextInput(attrs={"class": "form-control", "placeholder": "Університет, курси..."}),
            "languages": forms.TextInput(attrs={"class": "form-control", "placeholder": "Українська, Англійська..."}),
            "timezone": forms.Select(attrs={"class": "form-control"}, choices=TIMEZONE_CHOICES),
        }


class UserUpdateForm(forms.ModelForm):
    """Form for user account updates."""

    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "bio",
            "location",
            "website",
            "github_profile",
            "linkedin_profile",
            "hourly_rate",
            "is_available",
            "phone",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Розкажіть про себе..."}),
            "hourly_rate": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in {"is_available"}:
                field.widget.attrs.setdefault("class", "form-check-input")
            else:
                field.widget.attrs.setdefault("class", "form-control")
