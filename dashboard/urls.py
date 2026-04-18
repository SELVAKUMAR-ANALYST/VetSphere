from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_dashboard, name="admin_dashboard"),
    path("login/", views.AdminLoginView.as_view(), name="admin_login"),
    path("users/", views.admin_user_list, name="admin_user_list"),
    path("pets/", views.admin_pet_list, name="admin_pet_list"),
    path("messages/", views.admin_message_list, name="admin_message_list"),
    path("contact/", views.contact_view, name="contact_form_submit"),
]
