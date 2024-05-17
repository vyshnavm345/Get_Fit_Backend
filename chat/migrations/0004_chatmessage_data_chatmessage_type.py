# Generated by Django 5.0.3 on 2024-05-14 08:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0003_notification_seen"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatmessage",
            name="data",
            field=models.BinaryField(blank=True),
        ),
        migrations.AddField(
            model_name="chatmessage",
            name="type",
            field=models.CharField(blank=True, max_length=10),
        ),
    ]