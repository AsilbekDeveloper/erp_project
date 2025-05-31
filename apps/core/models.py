from django.db import models
from django.utils import timezone


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class SoftDeleteMixin(models.Model):
    is_active = models.BooleanField(default=True)

    def delete(self, **kwargs):
        self.is_active = False
        self.save(update_fields=["is_active", "updated_at"])

    class Meta:
        abstract = True
