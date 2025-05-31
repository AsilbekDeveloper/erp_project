from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedMixin


class Role(models.TextChoices):
    SUPERADMIN = "SUPERADMIN", "Super Admin"
    ADMIN = "ADMIN", "Admin"
    STAFF = "STAFF", "Staff / Employee"


class User(AbstractUser, TimeStampedMixin):
    role = models.CharField(max_length=15, choices=Role.choices, default=Role.STAFF)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_set",  # yangi related_name
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to.",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_set",  # yangi related_name
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    class Meta:
        indexes = [models.Index(fields=["role"])]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
