from django.urls import path
from .views import FitnessProgramCreateView, FitnessProgramListAPIView

urlpatterns = [
    path("create/", FitnessProgramCreateView.as_view()),
    path("retrive_all/", FitnessProgramListAPIView.as_view()),
   
]
