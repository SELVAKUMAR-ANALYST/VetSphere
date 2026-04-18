from django.http import JsonResponse
from billing.models import Invoice
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Booking, Attendance, Service
from .forms import BookingForm, ReviewForm
from django.contrib import messages
from django.db.models import Avg, Count
from django.utils import timezone


@login_required
def booking_list(request):
    if request.user.is_staff:
        bookings = Booking.objects.prefetch_related(
            "invoice_set", "invoice_set__payment_set"
        ).order_by("-start_time")
    else:
        bookings = (
            Booking.objects.filter(pet__owner=request.user)
            .prefetch_related("invoice_set", "invoice_set__payment_set")
            .order_by("-start_time")
        )
    return render(
        request, "bookings/booking_list.html", {"bookings": bookings}
    )


@login_required
def booking_create(request):
    if request.method == "POST":
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("booking_list")
    else:
        form = BookingForm(user=request.user)
    return render(request, "bookings/booking_form.html", {"form": form})


@login_required
def check_in(request, pk):
    if request.user.is_staff:
        booking = get_object_or_404(Booking, pk=pk)
    else:
        booking = get_object_or_404(Booking, pk=pk, pet__owner=request.user)
    
    attendance, created = Attendance.objects.get_or_create(booking=booking)
    attendance.check_in_time = timezone.now()
    attendance.save()
    booking.status = "checked_in"
    booking.save()
    return redirect("booking_list")


@login_required
def check_out(request, pk):
    if request.user.is_staff:
        booking = get_object_or_404(Booking, pk=pk)
    else:
        booking = get_object_or_404(Booking, pk=pk, pet__owner=request.user)
    
    attendance = get_object_or_404(Attendance, booking=booking)
    attendance.check_out_time = timezone.now()
    attendance.save()
    booking.status = "completed"
    booking.save()

    try:
        # Automated invoicing logic based on service price
        amount = booking.service.price if booking.service else 50.00
        Invoice.objects.get_or_create(booking=booking, defaults={"amount": amount})
        messages.success(request, "Pet checked out and invoice generated successfully.")
    except Exception as e:
        messages.error(request, f"Checked out, but an error occurred while generating the invoice. {e}")

    return redirect("booking_list")


@login_required
def booking_calendar(request):
    if request.user.is_staff:
        bookings = Booking.objects.order_by("-start_time")
    else:
        bookings = Booking.objects.filter(pet__owner=request.user).order_by(
            "-start_time"
        )
    return render(request, "bookings/calendar.html", {"bookings": bookings})


@login_required
def booking_events(request):
    if request.user.is_staff:
        bookings = Booking.objects.all()
    else:
        bookings = Booking.objects.filter(pet__owner=request.user)
    events = []
    for booking in bookings:
        color = "#3b82f6"  # blue
        if booking.status == "confirmed":
            color = "#10b981"  # green
        elif booking.status == "checked_in":
            color = "#f59e0b"  # yellow
        elif booking.status == "completed":
            color = "#6b7280"  # gray
        elif booking.status == "cancelled":
            color = "#ef4444"  # red

        events.append(
            {
                "title": f"{booking.pet.name} ({booking.get_status_display()})",
                "start": booking.start_time.isoformat(),
                "end": booking.end_time.isoformat(),
                "backgroundColor": color,
                "borderColor": color,
                "url": "/bookings/",  # Link to list or detail if exists
            }
        )
    return JsonResponse(events, safe=False)


@login_required
def add_review(request, booking_id):
    booking = get_object_or_404(
        Booking, id=booking_id, pet__owner=request.user
    )
    if booking.status != "completed":
        messages.error(request, "You can only review completed bookings.")
        return redirect("booking_list")

    if hasattr(booking, "review"):
        messages.warning(request, "You have already reviewed this booking.")
        return redirect("booking_list")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect("booking_list")
    else:
        form = ReviewForm()

    return render(
        request,
        "bookings/review_form.html",
        {"form": form, "booking": booking},
    )


def services_view(request):
    services = Service.objects.annotate(
        avg_rating=Avg("booking__review__rating"),
        review_count=Count("booking__review"),
    ).all()
    return render(request, "services.html", {"services": services})
