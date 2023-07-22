# Generated by Django 4.1.9 on 2023-07-21 17:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("announces", "0007_announcement_creation_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="announcement",
            name="creation_time",
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name="Data de criação"),
        ),
    ]