from django.urls import path
from . import views

urlpatterns = [
    path("", views.roster_list, name="roster_list"),
    path("<int:pk>/clock-in/", views.clock_in, name="clock_in"),
    path("<int:pk>/clock-out/", views.clock_out, name="clock_out"),
]
