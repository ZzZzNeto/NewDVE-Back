from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models
from django.utils.translation import gettext_lazy as _
from newdve_back.announces.models import Announcement, Tag

from newdve_back.users.managers import UserManager

class Address(models.Model):
    state = models.CharField(max_length=2)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255)
    number = models.CharField(max_length=10, blank=True, default="S/N")
    cep = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.pk} | {self.state} | {self.city} | {self.cep}'

class User(AbstractUser):
    COURSE_CHOICES = [
        ("ALIMENTOS", "Alimentos"),
        ("APICULTURA", "Apicultura"),
        ("INFORMATICA", "Informatica"),
        ("ADS", "Tecnologia em Análise e Desenvolvimento de Sistemas"),
        ("QUIMICA", "Quimica"),
        ("AGROINDUSTRIA", "Agroindustria"),
    ]

    SCHOOLING_CHOICES = [
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
    ]

    #ALL USERS
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    email = models.EmailField(_("email address"), unique=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    profile_picture = models.ImageField(upload_to ='profile_pictures/',  default='user_base.jpg')
    description = models.CharField(max_length=1000, null=True)
    contact_mail = models.EmailField(null=True)
    phone = models.CharField(max_length=200,null=True)
    instagram = models.CharField(max_length=20,null=True)
    linkedin = models.CharField(max_length=50,null=True)
    twitter = models.CharField(max_length=20,null=True)
    #CANDIDATE USER
    ocupattion = models.CharField(max_length=100, null=True)
    birth_date = models.DateField(null=True)
    preference_tags = models.ManyToManyField(Tag)
    portfolio = models.CharField(max_length=200, null=True)
    schooling = models.CharField(choices=SCHOOLING_CHOICES, null=True, max_length=20)
    saved_announcements = models.ManyToManyField(Announcement)
    #IFRN
    registration_ifrn = models.CharField(max_length=14, unique=True, null=True)
    course = models.CharField(choices=COURSE_CHOICES, null=True, max_length=100)
    #CREATOR USER
    cnpj = models.CharField(max_length=16,null=True)

    # First and last name do not cover name patterns around the globe
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    username = None  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    objects = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

class User_file(models.Model):
    file = models.FileField(upload_to ='files/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} | {self.user.name}'
    
class Notification(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    readed = models.BooleanField(default=False)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, null=True)