# Generated by Django 4.1.9 on 2023-05-20 18:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import newdve_back.users.managers


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("announces", "__first__"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
                ("name", models.CharField(blank=True, max_length=255, verbose_name="Name of User")),
                ("email", models.EmailField(max_length=254, unique=True, verbose_name="email address")),
                ("profile_picture", models.ImageField(null=True, upload_to="profile_pictures/")),
                ("description", models.CharField(max_length=1000, null=True)),
                ("contact_mail", models.EmailField(max_length=254, null=True)),
                ("phone", models.CharField(max_length=12, null=True)),
                ("instagram", models.CharField(max_length=20, null=True)),
                ("linkedin", models.CharField(max_length=50, null=True)),
                ("twitter", models.CharField(max_length=20, null=True)),
                ("ocupattion", models.CharField(max_length=100, null=True)),
                ("birth_date", models.DateField(null=True)),
                ("portfolio", models.CharField(max_length=200, null=True)),
                (
                    "schooling",
                    models.CharField(
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
                ("registration_ifrn", models.CharField(max_length=14, null=True, unique=True)),
                (
                    "course",
                    models.CharField(
                        choices=[
                            ("ALIMENTOS", "Alimentos"),
                            ("APICULTURA", "Apicultura"),
                            ("INFORMATICA", "Informatica"),
                            ("ADS", "Analise e desenvolvimento de sistemas"),
                            ("QUIMICA", "Quimica"),
                            ("AGROINDUSTRIA", "Agroindustria"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                ("cnpj", models.CharField(max_length=16, null=True)),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
            },
            managers=[
                ("objects", newdve_back.users.managers.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Address",
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
        migrations.CreateModel(
            name="User_file",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to="files/")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=30)),
                ("description", models.CharField(max_length=300)),
                ("readed", models.BooleanField(default=False)),
                (
                    "announcement",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.CASCADE, to="announces.announcement"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="address",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="users.address"),
        ),
        migrations.AddField(
            model_name="user",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                related_name="user_set",
                related_query_name="user",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="preference_tags",
            field=models.ManyToManyField(to="announces.tag"),
        ),
        migrations.AddField(
            model_name="user",
            name="saved_announcements",
            field=models.ManyToManyField(to="announces.announcement"),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
    ]
