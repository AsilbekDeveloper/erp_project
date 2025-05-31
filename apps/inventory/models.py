from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedMixin, SoftDeleteMixin


class Category(TimeStampedMixin):  # <-- SoftDeleteMixin olib tashlandi
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Warehouse(TimeStampedMixin):  # <-- SoftDeleteMixin olib tashlandi
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Product(TimeStampedMixin):
    sku = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    cost_price = models.DecimalField(max_digits=12, decimal_places=2)
    sell_price = models.DecimalField(max_digits=12, decimal_places=2)
    size = models.CharField(max_length=30, blank=True)
    color = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class StockMovement(TimeStampedMixin):
    class Type(models.TextChoices):
        IN = "IN", "Kirim"
        OUT = "OUT", "Chiqim"

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    movement_type = models.CharField(max_length=3, choices=Type.choices)
    quantity = models.PositiveIntegerField()

    class Meta:
        indexes = [models.Index(fields=["movement_type", "product"])]

    def __str__(self):
        return f"{self.product} {self.movement_type} {self.quantity}"
