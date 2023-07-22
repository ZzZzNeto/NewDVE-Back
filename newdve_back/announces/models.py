from django.db import models
from django.utils import timezone

# Create your models here.

class Tag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True)
    icon = models.ImageField()

    def __str__(self):
        return f'{self.pk} | {self.tag_name}'

class Announcement(models.Model):
    COURSE_CHOICES = [
        ("ALIMENTOS", "Alimentos"),
        ("APICULTURA", "Apicultura"),
        ("INFORMATICA", "Informatica"),
        ("ADS", "Analise e desenvolvimento de sistemas"),
        ("QUIMICA", "Quimica"),
        ("AGROINDUSTRIA", "Agroindustria"),
    ]

    company_name = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    schedule = models.CharField(max_length=30) #horario ex: 16h - 22h
    salary = models.FloatField(null=True)
    journey = models.CharField(max_length=100) #jornada de trabalho, ex: seg - sex
    vacancies = models.IntegerField()
    deadline = models.DateField()
    benefits = models.CharField(max_length=500, null=True)
    requeriments = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)
    address = models.ForeignKey("users.Address", on_delete=models.CASCADE)
    curriculum = models.BooleanField()
    course = models.CharField(choices=COURSE_CHOICES,max_length=100, null=True)
    total_workload = models.CharField(max_length=3, null=True)
    inscripts = models.ManyToManyField("users.User",related_name="inscripts", blank=True)
    creator = models.ForeignKey("users.User",related_name="criador", on_delete=models.CASCADE)
    creation_time = models.DateTimeField(verbose_name='Data de criação', default=timezone.now)
    rate = models.FloatField(default=0)

    def __str__(self):
        return f'{self.pk} | {self.company_name} | {self.creator.pk}'
    

class Announcement_image(models.Model):
    image = models.ImageField(upload_to ='announce_images/')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} | {self.announcement.company_name}'

class Rating(models.Model):

    rate = models.FloatField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, null=True)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, null=True)

    # def __str__(self):
    #     return f'{self.pk} | {self.user.name}({self.user.id}) | {self.announcement.company_name}({self.announcement.id})'
    

