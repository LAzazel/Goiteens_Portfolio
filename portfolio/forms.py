from django import forms
from .models import Order, Review
import datetime


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["client_name", "client_email", "client_phone", "title", "description", "budget", "deadline"]

    def clean_budget(self):
        b = self.cleaned_data.get("budget")
        if b is not None and b <= 0:
            raise forms.ValidationError("Бюджет повинен бути позитивним числом.")
        return b

    def clean_deadline(self):
        d = self.cleaned_data.get("deadline")
        if d and d < datetime.date.today():
            raise forms.ValidationError("Термін не може бути в минулому.")
        return d

    def clean(self):
        cleaned = super().clean()
        if not (cleaned.get("client_email") or cleaned.get("client_phone")):
            raise forms.ValidationError("Вкажіть email або телефон для контакту.")
        return cleaned


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["client_name", "text", "rating"]
        widgets = {
            "client_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваше ім'я"}),
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Ваш відгук"}),
            "rating": forms.NumberInput(attrs={"class": "form-control", "min": 1, "max": 5}),
        }

