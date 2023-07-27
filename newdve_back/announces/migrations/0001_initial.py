# Generated by Django 4.1.9 on 2023-05-20 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Announcement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("company_name", models.CharField(max_length=255)),
                ("schedule", models.CharField(max_length=30)),
                ("salary", models.FloatField(null=True)),
                ("journey", models.CharField(max_length=100)),
                ("vacancies", models.IntegerField()),
                ("deadline", models.DateField()),
                ("benefits", models.CharField(max_length=500, null=True)),
                ("requeriments", models.CharField(max_length=500, null=True)),
                ("description", models.CharField(max_length=500, null=True)),
                ("curriculum", models.BooleanField()),
                ("course", models.CharField(max_length=100, null=True)),
                ("total_workload", models.CharField(max_length=3, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("tag_name", models.CharField(max_length=50, unique=True)),
                ("icon", models.ImageField(upload_to="")),
            ],
        ),
        migrations.CreateModel(
            name="Rating",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "rate",
                    models.IntegerField(choices=[(1, "One"), (2, "Two"), (3, "Three"), (4, "Four"), (5, "Five")]),
                ),
                (
                    "announcement",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="announces.announcement"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Announcement_image",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="announce_images/")),
                (
                    "announcement",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="announces.announcement"),
                ),
            ],
        ),
        migrations.AddField(
            model_name="announcement",
            name="tags",
            field=models.ManyToManyField(to="announces.tag"),
        ),
    ]
