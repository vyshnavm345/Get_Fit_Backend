# Generated by Django 5.0.3 on 2024-04-22 11:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fitness_program", "0003_alter_fitnessprogram_category_lesson"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="program",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="lesson",
                to="fitness_program.fitnessprogram",
            ),
        ),
    ]
