import uuid
from django.conf import settings
from django.db import models

# Create your models here.
class Notification(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notifications", on_delete=models.CASCADE, blank=True)
    content = models.TextField(blank=True)
    has_seen = models.BooleanField(default=False, blank=True)