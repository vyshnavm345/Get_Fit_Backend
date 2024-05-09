from django.urls import path
from .views import (
    GetChatMessages
)

urlpatterns = [
    
    path("getMessages/<str:room_id>/", GetChatMessages.as_view()),
    
]
