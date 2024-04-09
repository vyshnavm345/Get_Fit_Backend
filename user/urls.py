from django.urls import path
from .views import (
    RegisterView,
    RetriveUserView,
    Retrive_full_user_data,
    update_user_profile,
    Verify_email,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("email_verification/", Verify_email.as_view(), name="email_verification"),
    path("me/", Retrive_full_user_data.as_view()),
    path("updateUser/", update_user_profile),
]
