from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'John', 'required': True}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Doe', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'john@example.com', 'required': True}),
            'phone': forms.TextInput(attrs={'placeholder': '+91 98765 43210', 'required': True}),
            'subject': forms.Select(choices=[
                ('', 'Select a subject'),
                ('appointment', 'Book an Appointment'),
                ('grooming', 'Grooming Services'),
                ('emergency', 'Emergency Care'),
                ('billing', 'Billing Enquiry'),
                ('other', 'Other'),
            ], attrs={'required': True}),
            'message': forms.Textarea(attrs={'placeholder': 'Tell us about your pet and how we can help...', 'required': True}),
        }
