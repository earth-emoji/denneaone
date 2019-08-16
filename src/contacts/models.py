import uuid
from django.conf import settings
from django.db import models
from django.utils.text import slugify

# Create your models here.
class Contact(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="contacts_made", on_delete=models.CASCADE, blank=True)
    target = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="contacts_accepts", on_delete=models.CASCADE, blank=True)

    @property
    def contact_room(self):
        return f"room_{self.initiator.id}_{self.target.id}_{self.slug}"


class ContactGroup(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    name = models.CharField(max_length=60, blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="contact_groups", on_delete=models.CASCADE, blank=True)
    contacts = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="contacts", blank=True)

    @property
    def slug_name(self):
        return slugify(self.name)

    @property
    def contact_group_room(self):
        return f"group_{self.slug_name}_{self.creator.id}_{self.slug}"


class ContactMessage(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="contact_messages", on_delete=models.CASCADE, blank=True)
    content = models.TextField(blank=True)