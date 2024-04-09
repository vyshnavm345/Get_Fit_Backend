from rest_framework import serializers
from .models import Trainer_profile

class TrainerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer_profile
        fields = ["specalized", "phone", "about", "certifications", "experience_years"]
