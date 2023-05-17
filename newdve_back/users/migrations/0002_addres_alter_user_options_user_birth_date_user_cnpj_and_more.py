# Generated by Django 4.1.9 on 2023-05-17 16:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("announces", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Addres",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("state", models.CharField(max_length=2)),
                ("city", models.CharField(max_length=50)),
                ("district", models.CharField(blank=True, max_length=255)),
                ("street", models.CharField(max_length=255)),
                ("number", models.CharField(blank=True, max_length=10)),
                ("cep", models.CharField(max_length=9)),
            ],
        ),
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "User", "verbose_name_plural": "Users"},
        ),
        migrations.AddField(
            model_name="user",
            name="birth_date",
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="cnpj",
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="contact_mail",
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="description",
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="instagram",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="linkedin",
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="ocupattion",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="phone",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="portfolio",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="preference_tags",
            field=models.ManyToManyField(to="announces.tag"),
        ),
        migrations.AddField(
            model_name="user",
            name="profile_picture",
            field=models.ImageField(null=True, upload_to="profile_pictures/"),
        ),
        migrations.AddField(
            model_name="user",
            name="saved_announces",
            field=models.ManyToManyField(to="announces.announce"),
        ),
        migrations.AddField(
            model_name="user",
            name="schooling",
            field=models.CharField(
                choices=[
                    ("NAO_ALFABETIZADO", "Não alfabetizado"),
                    ("EF_INCOMPLETO", "Ensino fundamental incompleto"),
                    ("EF_COMPLETO", "Ensino fundamental completo"),
                    ("CURSANDO_EF", "Cursando ensino fundamental"),
                    ("EM_INCOMPLETO", "Ensino médio incompleto"),
                    ("EM_COMPLETO", "Ensino médio completo"),
                    ("CURSANDO_EM", "Cursando ensino médio"),
                    ("ES_INCOMPLETO", "Ensino superior incompleto"),
                    ("ES_COMPLETO", "Ensino superior completo"),
                    ("CURSANDO_ES", "Cursando ensino superior"),
                    ("MESTRADO", "Mestrado"),
                    ("DOUTORADO", "Doutorado"),
                ],
                max_length=20,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="twitter",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.CreateModel(
            name="user_file",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to="files/")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="addres",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="users.addres"),
        ),
    ]
