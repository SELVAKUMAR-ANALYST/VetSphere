from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from pets.models import Pet
from bookings.models import Booking
from billing.models import Invoice
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from .models import ContactMessage
from .forms import ContactForm

User = get_user_model()


class AdminLoginView(LoginView):
    template_name = "dashboard/admin_login.html"
    redirect_authenticated_user = False

    def get_success_url(self):
        return reverse_lazy("admin_dashboard")


def is_admin(user):
    return user.is_superuser or user.is_staff


@user_passes_test(is_admin, login_url="admin_login")
def admin_dashboard(request):
    # Total counts
    total_users = User.objects.count()
    total_pets = Pet.objects.count()
    total_bookings = Booking.objects.count()
    total_messages = ContactMessage.objects.count()

    # Today's appointments
    today = timezone.now().date()
    todays_appointments = Booking.objects.filter(
        start_time__date=today
    ).order_by("start_time")

    # Total revenue from paid invoices
    total_revenue = (
        Invoice.objects.filter(status="paid").aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    # Data for charts (last 7 days bookings)
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    booking_counts = []
    labels = []
    for day in last_7_days:
        count = Booking.objects.filter(start_time__date=day).count()
        booking_counts.append(count)
        labels.append(day.strftime("%b %d"))

    # Service Popularity Data
    service_data_qs = Booking.objects.exclude(service__isnull=True).values('service__name').annotate(count=Count('id')).order_by('-count')
    service_labels = [item['service__name'] for item in service_data_qs]
    service_data = [item['count'] for item in service_data_qs]

    # Pet Demographics Data
    pet_data_qs = Pet.objects.values('breed').annotate(count=Count('id')).order_by('-count')
    # Limit to top 5 breeds, group rest as "Other"
    top_breeds = list(pet_data_qs[:5])
    other_breeds_count = sum(item['count'] for item in pet_data_qs[5:])
    pet_labels = [item['breed'] for item in top_breeds]
    pet_data = [item['count'] for item in top_breeds]
    if other_breeds_count > 0:
        pet_labels.append("Other")
        pet_data.append(other_breeds_count)

    # Monthly Revenue (Last 6 months)
    six_months_ago = today.replace(day=1) - timedelta(days=5*30) # approx
    six_months_ago = six_months_ago.replace(day=1)
    revenue_qs = Invoice.objects.filter(status='paid', issued_date__gte=six_months_ago)\
        .annotate(month=TruncMonth('issued_date'))\
        .values('month')\
        .annotate(monthly_total=Sum('amount'))\
        .order_by('month')
    
    revenue_labels = []
    revenue_data = []
    for item in revenue_qs:
        if item['month']:
            revenue_labels.append(item['month'].strftime("%b %Y"))
            revenue_data.append(float(item['monthly_total']))

    context = {
        "total_users": total_users,
        "total_pets": total_pets,
        "total_bookings": total_bookings,
        "todays_appointments": todays_appointments,
        "total_revenue": total_revenue,
        "chart_labels": labels,
        "chart_data": booking_counts,
        "service_labels": service_labels,
        "service_data": service_data,
        "pet_labels": pet_labels,
        "pet_data": pet_data,
        "revenue_labels": revenue_labels,
        "revenue_data": revenue_data,
        "total_messages": total_messages,
    }
    return render(request, "dashboard/admin_dashboard.html", context)


@user_passes_test(is_admin, login_url="admin_login")
def admin_user_list(request):
    users = User.objects.all().order_by("-date_joined")
    return render(request, "dashboard/admin_user_list.html", {"users": users})


@user_passes_test(is_admin, login_url="admin_login")
def admin_pet_list(request):
    pets = Pet.objects.all().order_by("-id")
    return render(request, "dashboard/admin_pet_list.html", {"pets": pets})


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "contact.html", {"success": True})
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})


@user_passes_test(is_admin, login_url="admin_login")
def admin_message_list(request):
    messages = ContactMessage.objects.all().order_by("-created_at")
    return render(
        request, "dashboard/admin_message_list.html", {"contact_messages": messages}
    )
