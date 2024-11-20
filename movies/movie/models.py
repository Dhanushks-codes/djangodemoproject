from django.db import models

# Create your models here.
class Movie(models.Model):
    title=models.CharField(max_length=20)
    description=models.CharField(max_length=50)
    language=models.CharField(max_length=20)
    year=models.IntegerField()
    cover=models.ImageField(upload_to="images")
