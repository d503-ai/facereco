from django.contrib.auth.models import User
from django.db import models


class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    first_image = models.ImageField()
    second_image = models.ImageField(blank=True)
    data_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user}"


class Neural(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    recognition_image_1 = models.ImageField(null=True)
    recognition_image_2 = models.ImageField(null=True)
    detect_image = models.ImageField()
    faces = models.IntegerField()
    euclidian_distance = models.FloatField(null=True)
    time = models.FloatField()
