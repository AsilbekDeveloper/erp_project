from django.db import models
from apps.core.models import TimeStampedMixin
from django.conf import settings
from apps.core.models import TimeStampedMixin
from apps.inventory.models import Category, Product


class ExpenseCategory(TimeStampedMixin):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Expense(TimeStampedMixin):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"{self.category} - {self.product} - {self.amount}"
