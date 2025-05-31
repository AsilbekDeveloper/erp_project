from django.contrib import admin
from .models import Customer, SaleOrder, SaleOrderLine


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("phone", "created_at", "updated_at")
    search_fields = ("phone",)
    ordering = ("-created_at",)


@admin.register(SaleOrder)
class SaleOrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "created_at", "updated_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
