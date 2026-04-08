from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

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
