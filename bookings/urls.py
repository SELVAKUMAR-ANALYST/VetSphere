from django.urls import path
from . import views

urlpatterns = [
    path("", views.booking_list, name="booking_list"),
    path("new/", views.booking_create, name="booking_create"),
    path("calendar/", views.booking_calendar, name="booking_calendar"),
    path("calendar/events/", views.booking_events, name="booking_events"),
    path("<int:pk>/check-in/", views.check_in, name="check_in"),
    path("<int:pk>/check-out/", views.check_out, name="check_out"),
    path("review/<int:booking_id>/", views.add_review, name="add_review"),
]
