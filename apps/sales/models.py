from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedMixin
from apps.inventory.models import Product


class Customer(TimeStampedMixin):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()


class SaleOrder(TimeStampedMixin):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    cashier = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    note = models.CharField(max_length=255, blank=True)

    @property
    def total(self):
        return sum(line.subtotal for line in self.lines.all())

    def __str__(self):
        return f"SO-{self.pk}"


class SaleOrderLine(models.Model):
    order = models.ForeignKey(SaleOrder, related_name="lines", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def subtotal(self):
        return self.price * self.quantity
