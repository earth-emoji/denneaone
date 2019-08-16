import uuid
from django.db import models
from django.shortcuts import reverse

from accounts.models import Customer, Vendor
from catalog.models import Product

# Create your models here.
class Event(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    name = models.CharField(max_length=50, blank=True)
    details = models.TextField(blank=True)
    venue = models.CharField(max_length=200, blank=True)
    date = models.DateField(help_text='Please use the following format: <em>YYYY-MM-DD</em>.', blank=True)
    time = models.TimeField(help_text='Please use the following format: <em>HH:MM:SS<em>', blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='events', blank=True)
    attendees = models.ManyToManyField(Customer, related_name='events', blank=True)

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'
        ordering = ['date', 'time']

    def get_absolute_url(self):
        return reverse('events:event-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    def get_number_of_attendees(self):
        return self.attendees.all().count()

class Ticket(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets", blank=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.product.name