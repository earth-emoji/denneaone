from django import forms
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect

from .models import Product, Reservation


class ProductForm(forms.ModelForm):
    name = forms.CharField(max_length=128, min_length=2, strip=True, widget=forms.TextInput(
        attrs={'class ': 'form-control rounded-pill '}))
    description = forms.CharField(
        strip=True, widget=forms.Textarea(attrs={'class ': 'form-control'}))
    stock_quantity = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control rounded-pill '}))
    price = forms.DecimalField(max_digits=6, decimal_places=2, widget=forms.NumberInput(
        attrs={'class': 'form-control rounded-pill '}))

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'stock_quantity',
            'price',
        ]


class ServiceForm(forms.ModelForm):
    DURATION_MEASURE_CHOICES = (
        ('DAY', 'Day'),
        ('HOUR', 'Hour'),
    )
    name = forms.CharField(max_length=128, min_length=2, strip=True,
                           widget=forms.TextInput(attrs={'class ': 'form-control'}))
    price = forms.DecimalField(max_digits=6, decimal_places=2,
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    duration_measure = forms.CharField(max_length=128, min_length=2, widget=forms.Select(
        attrs={'class ': 'form-control'}, choices=DURATION_MEASURE_CHOICES))

    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'duration_measure',
        ]


class ReservationForm(forms.ModelForm):
    reserved_start_date = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}))
    reserved_start_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'class': 'form-control', 'type': 'time'}))
    reserved_end_date = forms.DateField(widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date'}))
    reserved_end_time = forms.TimeField(widget=forms.TimeInput(
        attrs={'class': 'form-control', 'type': 'time'}))

    class Meta:
        model = Reservation
        fields = [
            'reserved_start_date',
            'reserved_start_time',
            'reserved_end_date',
            'reserved_end_time',
        ]

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop('product')
        super(ReservationForm, self).__init__(*args, **kwargs)

    def clean(self):
        # Then call the clean() method of the super  class
        cleaned_data = super(ReservationForm, self).clean()
        # ... do some cross-fields validation for the subclass
        reserved_start_date = cleaned_data.get('reserved_start_date')
        reserved_start_time = cleaned_data.get('reserved_start_time')
        reserved_end_date = cleaned_data.get('reserved_end_date')
        reserved_end_time = cleaned_data.get('reserved_end_time')

        if Reservation.objects.filter(product=self.product, reserved_start_date=reserved_start_date, reserved_start_time=reserved_start_time, reserved_end_date=reserved_end_date, reserved_end_time=reserved_end_time).exists():
            raise forms.ValidationError('Please choose another time')

        # Finally, return the cleaned_data
        return cleaned_data
