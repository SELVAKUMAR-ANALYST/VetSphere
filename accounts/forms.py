from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import CustomerProfile

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "style": "width: 100%; padding: 0.75rem; "
                    "border: 1px solid var(--border); "
                    "border-radius: 0.5rem; outline: none; "
                    "box-sizing: border-box;",
                    "placeholder": f"Enter {field.label.lower()}" if field.label else f"Enter {field_name}",
                }
            )

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ("billing_address",)
        widgets = {
            "billing_address": forms.Textarea(
                attrs={
                    "style": "width: 100%; padding: 0.75rem; border: 1px solid var(--border); border-radius: 0.5rem; outline: none; box-sizing: border-box; min-height: 120px;",
                    "placeholder": "e.g. 15, Gandhi Nagar Main Road, Chennai - 600020",
                }
            )
        }
        labels = {
            "billing_address": "Billing Address (For Invoices)"
        }
