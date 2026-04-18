from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomerProfileForm
from .models import CustomerProfile
from django.contrib.auth import get_user_model
from pets.models import Pet, VaccinationRecord
from bookings.models import Booking
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("dashboard")
        messages.error(
            request, "Unsuccessful registration. Invalid information."
        )
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect("admin_dashboard")
    
    pets = Pet.objects.filter(owner=request.user)
    bookings = Booking.objects.filter(pet__owner=request.user).order_by(
        "-start_time"
    )[:5]

    # Vaccination alerts: expiring in less than 30 days
    upcoming_limit = timezone.now().date() + timedelta(days=30)
    alerts = VaccinationRecord.objects.filter(
        pet__owner=request.user, expiry_date__lte=upcoming_limit
    ).order_by("expiry_date")

    # Latest Invoice
    from billing.models import Invoice

    latest_invoice = (
        Invoice.objects.filter(booking__pet__owner=request.user)
        .order_by("-issued_date")
        .first()
    )

    # Chart Data: Bookings over the last 6 months
    six_months_ago = timezone.now().date() - timedelta(days=180)
    booking_counts = (
        Booking.objects.filter(
            pet__owner=request.user, start_time__date__gte=six_months_ago
        )
        .annotate(month=TruncMonth("start_time"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    chart_labels = [item["month"].strftime("%b %Y") for item in booking_counts]
    chart_data = [item["count"] for item in booking_counts]

    context = {
        "pets": pets,
        "recent_bookings": bookings,
        "alerts": alerts,
        "latest_invoice": latest_invoice,
        "today": timezone.now().date(),
        "chart_labels": chart_labels,
        "chart_data": chart_data,
    }
    return render(request, "dashboard.html", context)


def forgot_password(request):
    User = get_user_model()
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not new_password or not confirm_password:
            messages.error(request, "All fields are required.")
        elif new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
        else:
            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password reset successful! Please login with your new password.")
                return redirect("login")
            except User.DoesNotExist:
                messages.error(request, "No account found with that username.")

    return render(request, "accounts/forgot_password.html")


@login_required
def profile_settings(request):
    if request.user.is_staff:
        # Prevent staff from using customer profile settings
        return redirect("admin_dashboard")
        
    profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your billing address has been successfully updated!")
            return redirect("dashboard")
    else:
        form = CustomerProfileForm(instance=profile)
        
    return render(request, "accounts/profile_settings.html", {"form": form})
