# Generated by Django 5.0.3 on 2024-05-09 04:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0009_alter_followedprograms_created_on"),
    ]

    operations = [
        migrations.AddField(
            model_name="useraccount",
            name="logged_in",
            field=models.BooleanField(default=False),
        ),
    ]
