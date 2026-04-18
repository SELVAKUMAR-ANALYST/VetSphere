from django import forms
from .models import Pet, DailyLog, HealthLog


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ["name", "pet_type", "breed", "age", "medical_info", "image"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Enter pet name (e.g., Buddy)"}
            ),
            "pet_type": forms.Select(
                attrs={"class": "form-input"}
            ),
            "breed": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Enter pet breed (e.g., Golden Retriever)"}
            ),
            "age": forms.NumberInput(
                attrs={"class": "form-input", "placeholder": "Age in years", "min": "0"}
            ),
            "medical_info": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "placeholder": "Enter any important medical information or history...",
                    "rows": 3,
                }
            ),
        }


class DailyLogForm(forms.ModelForm):
    class Meta:
        model = DailyLog
        fields = ["activity_type", "notes"]
        widgets = {
            "activity_type": forms.Select(attrs={"class": "form-input"}),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "placeholder": "What did the pet do?",
                    "rows": 3,
                }
            ),
        }


class HealthLogForm(forms.ModelForm):
    class Meta:
        model = HealthLog
        fields = ["log_type", "date", "description", "veterinarian_name", "follow_up_required", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-input"}),
            "log_type": forms.Select(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"class": "form-input", "rows": 2}),
            "veterinarian_name": forms.TextInput(attrs={"class": "form-input"}),
            "notes": forms.Textarea(attrs={"class": "form-input", "rows": 2}),
        }
