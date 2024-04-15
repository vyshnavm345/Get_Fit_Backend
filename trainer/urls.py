from django.urls import path
from .views import TrainerProfileView, RetriveTrainerProfile, RetriveAllTrainers

urlpatterns = [
    path("TrainerProfileCreation/", TrainerProfileView.as_view()),
    path("getTrainer/", RetriveTrainerProfile.as_view()),
    path("allTrainer/", RetriveAllTrainers.as_view()),
]
