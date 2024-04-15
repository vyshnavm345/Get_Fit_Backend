from django.db import models
from django.utils import timezone
from trainer.models import Trainer_profile

class FitnessProgram(models.Model):
    PROGRAM_CATEGORIES = [
        ("Cardio", "Cardio"),
        ("Strength Training", "Strength Training"),
        ("Yoga", "Yoga"),
        ("Pilates", "Pilates"),
        ("HIIT", "HIIT"),
        ("CrossFit", "CrossFit"),
        ("Other", "Other"),
    ]
    
    LEVEL_CHOICES = [
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advance", "Advance"),
    ]
    
    
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default="Beginner")
    program_name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in days")
    trainer = models.ForeignKey(Trainer_profile, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    cover_image = models.ImageField(upload_to="fitness_programs/images", null=True, blank=True)
    category = models.CharField(max_length=50, choices=PROGRAM_CATEGORIES, default="Other")
    
    def __str__(self):
        return self.program_name
    
# class Media(models.Model):
#     url = models.URLField()
#     program = models.ForeignKey(FitnessProgram, on_delete=models.CASCADE, related_name='media')
    
#     def __str__(self):
#         return self.url