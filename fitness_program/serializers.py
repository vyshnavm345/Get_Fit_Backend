from rest_framework import serializers
from .models import FitnessProgram

class FitnessProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessProgram
        fields = '__all__'