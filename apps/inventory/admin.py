from django.contrib import admin
from .models import Category, Warehouse, Product, StockMovement


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("-created_at",)


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("-created_at",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "created_at")
    list_filter = ("category",)
    search_fields = ("name", "category__name")
    ordering = ("-created_at",)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("product", "warehouse", "quantity", "movement_type", "created_at")
    list_filter = ("warehouse", "movement_type")
    search_fields = ("product__name", "warehouse__name")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
