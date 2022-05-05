from django.db import models


class Result(models.Model):
    title = models.CharField(max_length=200)
    first_image = models.ImageField()
    second_image = models.ImageField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title