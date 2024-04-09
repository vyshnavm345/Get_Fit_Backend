from django.db import models
from user.models import UserAccount
# Create your models here.
# import csv

# countries = []

# # Open the CSV file
# with open('countries.csv', mode='r', encoding='utf-8-sig') as file:
#     # Create a CSV reader object
#     csv_reader = csv.DictReader(file)
    
#     # Iterate over each row in the CSV file
#     for row in csv_reader:
#         # Append a tuple of alpha-3 code and country name to the list
#         countries.append((row['alpha-3'], row['country']))

# # Sort countries alphabetically by country name
# countries.sort(key=lambda x: x[1])

# # Ensure unique countries
# countries = list(set(countries))

class Trainer_profile(models.Model):
    CHOICES = [
        ("General_fitness", "General_fitness"),
        ("yoga", "Yoga"),
        ("meditation", "Meditation"),
        ("diet", "Diet"),
        ("calisthenics", "Calisthenics"),
        ("weight_training", "Weight Training"),
        ("Cardio", "Cardio"),
        ("Other", "Other"),
    ]
    user = models.OneToOneField(
        UserAccount,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="trainer_profile"
    )
    specalized = models.CharField(
        max_length=50, choices=CHOICES, default="General_fitness"
    )
    phone = models.CharField(max_length=50, blank=True, null=True)
    # country = models.CharField(max_length=50,choices=countries, null=True, blank=True)
    about = models.CharField(max_length=700, null=True, blank=True)
    certifications = models.CharField(max_length=255, blank=True, null=True)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return self.user.first_name