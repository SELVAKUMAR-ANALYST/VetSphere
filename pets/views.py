from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Pet
from .forms import PetForm, DailyLogForm, HealthLogForm


@login_required
def pet_list(request):
    query = request.GET.get('q')
    pets = Pet.objects.filter(owner=request.user)
    
    if query:
        pets = pets.filter(
            Q(name__icontains=query) | 
            Q(breed__icontains=query)
        )
        
    return render(request, "pets/pet_list.html", {"pets": pets, "query": query})


@login_required
def pet_create(request):
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            return redirect("pet_list")
    else:
        form = PetForm()
    return render(request, "pets/pet_form.html", {"form": form})


@login_required
def pet_update(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect("pet_list")
    else:
        form = PetForm(instance=pet)
    return render(request, "pets/pet_form.html", {"form": form})


@login_required
def pet_delete(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == "POST":
        pet.delete()
        return redirect("pet_list")
    return render(request, "pets/pet_confirm_delete.html", {"pet": pet})


@login_required
def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    logs = pet.daily_logs.all()
    health_logs = pet.health_logs.all()
    
    if request.method == "POST":
        # Handle Daily Log simple submission
        if 'activity_type' in request.POST:
            log_form = DailyLogForm(request.POST)
            if log_form.is_valid():
                log = log_form.save(commit=False)
                log.pet = pet
                log.logged_by = request.user
                log.save()
                return redirect("pet_detail", pk=pk)
    
    log_form = DailyLogForm()
    health_form = HealthLogForm()
    
    return render(
        request,
        "pets/pet_detail.html",
        {
            "pet": pet, 
            "logs": logs, 
            "health_logs": health_logs,
            "log_form": log_form, 
            "health_form": health_form
        },
    )


@login_required
def add_health_log(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == "POST":
        form = HealthLogForm(request.POST)
        if form.is_valid():
            health_log = form.save(commit=False)
            health_log.pet = pet
            health_log.save()
            return redirect("pet_detail", pk=pk)
    return redirect("pet_detail", pk=pk)
