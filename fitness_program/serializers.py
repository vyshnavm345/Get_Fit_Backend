from rest_framework import serializers
from .models import FitnessProgram, Lesson

class FitnessProgramSerializer(serializers.ModelSerializer):
    trainer_name = serializers.SerializerMethodField()
    class Meta:
        model = FitnessProgram
        fields = '__all__'
        
    def get_trainer_name(self, obj):
        # print("the returned full name is ", obj.trainer.user.fullname())
        return obj.trainer.user.fullname()
        
class ProgrammeLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'