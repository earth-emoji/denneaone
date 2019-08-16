from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.db import transaction
from django.forms.utils import ValidationError

from accounts.models import Vendor, Customer
from users.models import User


class CustomerSignUpForm(UserCreationForm):
    username = forms.CharField(min_length=1, max_length=30, widget=forms.TextInput(attrs={'class': 'form-control rounded-pill mb-3', 'placeholder': 'Username'}))
    email = forms.CharField(min_length=1, max_length=60, widget=forms.EmailInput(attrs={'class': 'form-control rounded-pill mb-3', 'placeholder': 'Email'}))
    name = forms.CharField(min_length=1, max_length=60, widget=forms.TextInput(attrs={'class': 'form-control rounded-pill mb-3', 'placeholder': 'Name'}))
    photo = forms.ImageField(widget=forms.FileInput(attrs={'class': 'inputfile inputfile-custom'}))
    password1 = forms.CharField(min_length=1, max_length=60, widget=forms.PasswordInput(attrs={'class': 'form-control rounded-pill mb-3', 'placeholder': 'Password'}))
    password2 = forms.CharField(min_length=1, max_length=60, widget=forms.PasswordInput(attrs={'class': 'form-control rounded-pill mb-3', 'placeholder': 'Confirm Password'}))

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'name', 'email', 'photo')

    # @transaction.atomic
    def save(self):
        user = super().save()
        Customer.objects.create(user=user)
        return user