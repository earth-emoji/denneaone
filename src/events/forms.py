from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    name = forms.CharField(max_length=50, min_length=3, widget=forms.TextInput(attrs={'class':'form-control'}))
    venue = forms.CharField(max_length=200, min_length=3, widget=forms.TextInput(attrs={'class':'form-control'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'class':'form-control', 'type': 'time'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control', 'type': 'date'}))
    details = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model = Event
        fields = ('name', 'details', 'venue', 'time', 'date',)