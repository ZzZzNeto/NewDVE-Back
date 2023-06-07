# Generated by Django 4.1.9 on 2023-05-20 18:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("announces", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="announcement",
            name="address",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to="users.address"),
        ),
        migrations.AddField(
            model_name="announcement",
            name="creator",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="criador",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="announcement",
            name="inscripts",
            field=models.ManyToManyField(related_name="inscripts", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="rating",
            name="user",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]