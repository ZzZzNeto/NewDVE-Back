# Generated by Django 4.1.9 on 2023-06-16 16:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="cep",
            field=models.CharField(max_length=10),
        ),
    ]
