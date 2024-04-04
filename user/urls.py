from django.urls import path
from .views import RegisterView, RetriveUserView, Retrive_full_user_data, update_user_profile

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('me/', Retrive_full_user_data.as_view()),
    path('updateUser/', update_user_profile),
    
]