from django import forms

from .models import Photo

class PhotoForm(forms.ModelForm):
    url = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}))

    class Meta:
        model = Photo
        fields = ('url',)
