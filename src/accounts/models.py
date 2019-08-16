import uuid
from django.conf import settings
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from . import choices

class CustomerManager(models.Manager):
    use_for_related_fields = True


class Customer(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="customer", on_delete=models.CASCADE, blank=True)
    customer_type = models.CharField(max_length=30, choices=choices.CUSTOMER_TYPE_CHOICES, blank=True)
    objects = CustomerManager()

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')

    def __str__(self):
        return self.user.username

class VendorManager(models.Manager):
    use_for_related_fields = True

# Create your models here. 
class Vendor(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="vendor", on_delete=models.CASCADE)
    business_name = models.CharField(unique=True, max_length=255, null=True, blank=True)
    active = models.BooleanField(default=False)

    objects = VendorManager()

    class Meta:
        verbose_name = _('vendor')
        verbose_name_plural = _('vendors')

    def __str__(self):
        return self.business_name
