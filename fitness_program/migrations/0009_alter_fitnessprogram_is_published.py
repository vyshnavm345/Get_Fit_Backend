# Generated by Django 5.0.3 on 2024-05-17 05:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fitness_program", "0008_fitnessprogram_is_published"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fitnessprogram",
            name="is_published",
            field=models.BooleanField(default=False),
        ),
    ]
