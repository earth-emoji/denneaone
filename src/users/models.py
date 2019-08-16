import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import AppUserManager
from addresses.models import Address


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_id/<filename>
    return '{0}/{1}'.format(instance.username, filename)

# Create your models here.


class Acl(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    # fields removed from base user model
    first_name = None
    last_name = None

    SEX_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    username = models.CharField(max_length=30, unique=True, blank=True)
    email = models.EmailField(_('email address'), unique=True, blank=True)
    photo = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True)
    name = models.CharField('full name', max_length=255, blank=True)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    sex = models.CharField(
        max_length=6, choices=SEX_CHOICES, null=True, blank=True)
    acl = models.ForeignKey(Acl, related_name='users',
                            on_delete=models.DO_NOTHING, null=True, blank=True)
    addresses = models.ManyToManyField(
        Address, related_name='addresses', blank=True)
    is_vendor = models.BooleanField(default=False, blank=True)
    is_customer = models.BooleanField(default=False, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email']

    objects = AppUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.username

    @property
    def notification_channel(self):
        return f"notify_{self.username}"
