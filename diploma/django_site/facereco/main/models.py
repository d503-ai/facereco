from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Record(models.Model):
    NOISE_CHOICES = [
        ('gaussian', 'Gauss Noise'),
        ('laplacian', 'Laplacian Noise'),
        ('poisson', 'Poisson Noise'),
        ('impulse', 'Impulse Noise'),
        ('none', 'No Noise'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    first_image = models.ImageField(blank=True, null=True)
    second_image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    noise_type = models.CharField(max_length=10, choices=NOISE_CHOICES, default='none')
    noise_applied = models.BooleanField(default=False)
    attenuate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Neural(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    recognition_image_1 = models.ImageField(null=True)
    recognition_image_2 = models.ImageField(null=True)
    faces = models.IntegerField()
    euclidian_distance = models.FloatField(null=True)
    time = models.FloatField()
