from django import forms
from .models import Record, Neural


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['title', 'first_image', 'second_image', 'noise_type', 'attenuate']


class NeuralForm(forms.ModelForm):
    class Meta:
        model = Neural
        fields = ['title', 'record', 'recognition_image_1', 'recognition_image_2', 'faces',
                  'euclidian_distance', 'time']