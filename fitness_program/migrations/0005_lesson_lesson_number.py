# Generated by Django 5.0.3 on 2024-04-27 09:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fitness_program", "0004_alter_lesson_program"),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="lesson_number",
            field=models.PositiveIntegerField(default=0, unique=True),
            preserve_default=False,
        ),
    ]
