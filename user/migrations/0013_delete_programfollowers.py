# Generated by Django 5.0.3 on 2024-05-16 06:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0012_programfollowers"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ProgramFollowers",
        ),
    ]
