from django import forms
from .models import Record, Neural


class ImageForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = [
            'first_image',
            'second_image'
        ]


class NeuralForm(forms.ModelForm):
    class Meta:
        model = Neural
        fields = [
            'title',
            'recognition_image_1',
            'recognition_image_2',
            'detect_image',
            'time',
            'euclidian_distance',
        ]
