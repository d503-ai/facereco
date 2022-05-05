from django import forms
from .models import Result


class ImageForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = '__all__'