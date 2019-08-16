import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Country(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    name = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=5, blank=True)

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')

    def __str__(self):
        return self.name


class State(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    nname = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=5, blank=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, related_name='states', blank=True)

    class Meta:
        verbose_name = _('state')
        verbose_name_plural = _('states')

    def __str__(self):
        return self.name


class City(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    name = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=5, blank=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING, related_name='cities', blank=True)

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')

    def __str__(self):
        return self.name


class Address(models.Model):
    ADDRESS_TYPE_CHOICES = (
        ('Billing', 'Billing'),
        ('Business', 'Business'),
        ('Primary', 'Primary'),
        ('Shipping', 'Shipping'),
    )
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    line1 = models.CharField(max_length=100, blank=True)
    line2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, related_name='addresses')
    suite = models.CharField(max_length=10, null=True, blank=True)
    postal_code = models.CharField(max_length=12, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    address_type = models.CharField(max_length=11, choices=ADDRESS_TYPE_CHOICES, blank=True)

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')

    def __str__(self):
        return f"{self.line1}, {self.city.name}, {self.city.state.name}"

