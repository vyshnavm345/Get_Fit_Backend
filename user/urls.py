from django.urls import path
from .views import (
    RegisterView,
    RetriveUserView,
    Retrive_full_user_data,
    update_user_profile,
    Verify_email,
    GetFollowedPrograms,
    GetUserById,
    FollowProgram
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("email_verification/", Verify_email.as_view(), name="email_verification"),
    path("me/", Retrive_full_user_data.as_view()),
    path("updateUser/", update_user_profile),
    path("getFollowedPrograms/", GetFollowedPrograms.as_view()),
    path("getUserById/<int:id>/", GetUserById.as_view()),
    path("followProgram/<int:id>/", FollowProgram.as_view()),
]
