from django.db import models

# Create your models here.

class Tag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True)
    icon = models.ImageField()

    def __str__(self):
        return f'{self.pk} | {self.tag_name}'

class Announce(models.Model):
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
    addres = models.ForeignKey("users.Addres", on_delete=models.CASCADE)
    curriculum = models.BooleanField()
    course = models.CharField(max_length=100, null=True)
    total_workload = models.CharField(max_length=3, null=True)
    inscripts = models.ManyToManyField("users.User",related_name="inscripts")
    creator = models.ForeignKey("users.User",related_name="criador", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} | {self.company_name} | {self.creator.pk}'
    

class Announce_image(models.Model):
    image = models.ImageField(upload_to ='announce_images/')
    announce = models.ForeignKey(Announce, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} | {self.announce.company_name}'

class Rating(models.Model):
    STARS = [
        (1, "One"),
        (2, "Two"),
        (3, "Three"),
        (4, "Four"),
        (5, "Five"),
    ]

    rate = models.IntegerField(choices=STARS)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    announce = models.ForeignKey(Announce, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} | {self.user.name} | {self.announce.pk}'
    

