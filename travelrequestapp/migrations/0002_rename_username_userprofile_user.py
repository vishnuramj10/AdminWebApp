# Generated by Django 5.0.4 on 2024-04-30 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("travelrequestapp", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userprofile",
            old_name="Username",
            new_name="user",
        ),
    ]
