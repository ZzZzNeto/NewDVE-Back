# Generated by Django 4.1.9 on 2023-07-22 19:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("announces", "0009_announcement_rate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rating",
            name="rate",
            field=models.BooleanField(),
        ),
    ]