from django.urls import path
from .views import TrainerProfileView

urlpatterns = [
    path("TrainerProfileCreation/", TrainerProfileView.as_view())
]
