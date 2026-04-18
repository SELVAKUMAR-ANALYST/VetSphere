from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Shift, Timesheet
from django.utils import timezone


@login_required
def roster_list(request):
    # If staff, show all shifts. If client, show nothing or just a message.
    if request.user.is_staff_member:
        shifts = Shift.objects.all().order_by("start_time")
    else:
        shifts = Shift.objects.filter(staff=request.user).order_by(
            "start_time"
        )
    return render(request, "rosters/roster_list.html", {"shifts": shifts})


@login_required
def clock_in(request, pk):
    shift = get_object_or_404(Shift, pk=pk, staff=request.user)
    timesheet, created = Timesheet.objects.get_or_create(shift=shift)
    timesheet.clocked_in = timezone.now()
    timesheet.save()
    return redirect("roster_list")


@login_required
def clock_out(request, pk):
    shift = get_object_or_404(Shift, pk=pk, staff=request.user)
    timesheet = get_object_or_404(Timesheet, shift=shift)
    timesheet.clocked_out = timezone.now()
    timesheet.save()
    return redirect("roster_list")
