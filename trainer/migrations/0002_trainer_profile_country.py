# Generated by Django 5.0.3 on 2024-04-09 05:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("trainer", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="trainer_profile",
            name="country",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
