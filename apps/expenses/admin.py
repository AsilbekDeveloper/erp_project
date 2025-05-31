from django.contrib import admin

from .models import Expense, ExpenseCategory


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    ordering = ("-created_at",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("category", "product", "amount", "user", "created_at")
    list_filter = ("category", "user")
    search_fields = ("category__name", "product__name", "note")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
