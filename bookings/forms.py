from django import forms
from .models import Booking, Review
from pets.models import Pet


class BookingForm(forms.ModelForm):
    pet = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-input", "placeholder": "Enter pet's name"}
        ),
        label="Pet Name",
    )

    class Meta:
        model = Booking
        fields = ["pet", "service", "start_time", "end_time"]
        widgets = {
            "service": forms.Select(attrs={"class": "form-input", "required": True}),
            "start_time": forms.DateTimeInput(
                attrs={"class": "form-input", "type": "datetime-local", "required": True}
            ),
            "end_time": forms.DateTimeInput(
                attrs={"class": "form-input", "type": "datetime-local", "required": True}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(BookingForm, self).__init__(*args, **kwargs)

        # If editing an existing booking, show the pet's name in the text field
        if self.instance and self.instance.pk and self.instance.pet:
            self.initial["pet"] = self.instance.pet.name

    def clean_pet(self):
        pet_name = self.cleaned_data.get("pet")
        if not self.user:
            raise forms.ValidationError("User context is required.")

        # Use filter().first() to avoid MultipleObjectsReturned if pets have same name
        pet = Pet.objects.filter(
            owner=self.user, name__iexact=pet_name
        ).first()

        if not pet:
            raise forms.ValidationError(
                f"No pet named '{pet_name}' found for your account. Please register your pet first."
            )
        return pet

    def clean(self):
        cleaned_data = super().clean()
        pet = cleaned_data.get("pet")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time:
            if start_time >= end_time:
                raise forms.ValidationError(
                    "End time must be after start time."
                )

            # Check for overlapping bookings for the same service (excluding cancelled)
            overlap = Booking.objects.filter(
                service=cleaned_data.get("service"),
                start_time__lt=end_time,
                end_time__gt=start_time,
            ).exclude(status__in=["cancelled"])

            if self.instance.pk:
                overlap = overlap.exclude(pk=self.instance.pk)

            if overlap.exists():
                raise forms.ValidationError(
                    "This time slot is already fully booked. Please select another time."
                )

        return cleaned_data


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(attrs={"class": "form-input"}),
            "comment": forms.Textarea(
                attrs={
                    "class": "form-input",
                    "placeholder": "Tell us about your experience...",
                    "rows": 3,
                }
            ),
        }
