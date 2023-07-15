from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _


class Label(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
